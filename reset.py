"""
    Reset (undo last throw) functionality.

    1) Validate project and .pebble files exist.
    2) Load current head_commit from project_info.json.
    3) Find the current throw in project_throws.json.
    4) Get last_throw_id from current throw.
    5) Find the previous throw object.
    6) Restore files to previous throw's file_contents.
    7) Delete files not present in previous throw.
    8) Update project_info.json (head_commit, file_hashes).
    9) Print confirmation.
"""
import os
import json
from tinydb import TinyDB, Query

def validate_project(project_path: str) -> bool:
    """
    Validate that the project path exists and contains a .pebble directory with necessary files.
    
    Args:
        project_path (str): The full path to the project folder.
    
    Returns:
        bool: True if valid, False otherwise.
    """
    pebble_dir = os.path.join(project_path, ".pebble")
    if not os.path.isdir(pebble_dir):
        print(f"Error: .pebble directory not found in {project_path}.")
        return False
    
    required_files = ["project_info.json", "project_throws.json"]
    for file in required_files:
        if not os.path.isfile(os.path.join(pebble_dir, file)):
            print(f"Error: Required file {file} not found in .pebble directory.")
            return False
    
    return True

def reset_to_previous_throw(project_path: str):
    """
    Reset the project to the previous throw (undo last throw).
    """
    import shutil
    pebble_dir = os.path.join(project_path, ".pebble")
    info_path = os.path.join(pebble_dir, "project_info.json")
    throws_path = os.path.join(pebble_dir, "project_throws.json")

    # 1. Validate
    if not validate_project(project_path):
        return

    # 2. Load current head_commit
    db = TinyDB(info_path)
    if len(db) == 0:
        print("Error: project_info.json is empty.")
        db.close()
        return
    info = db.all()[0]
    head_commit = info.get("head_commit")
    db.close()
    if not head_commit:
        print("Error: No head_commit found.")
        return

    # 3. Find current throw
    db = TinyDB(throws_path)
    throws = db.all()
    current_throw = None
    for t in throws:
        if t.get("throw_id") == head_commit:
            current_throw = t
            break
    if not current_throw:
        print(f"Error: Throw with id {head_commit} not found.")
        db.close()
        return

    # 4. Get last_throw_id
    last_throw_id = current_throw.get("last_throw_id")
    if not last_throw_id:
        print("Error: No previous throw to reset to.")
        db.close()
        return

    # 5. Find previous throw object
    prev_throw = None
    for t in throws:
        if t.get("throw_id") == last_throw_id:
            prev_throw = t
            break
    db.close()
    if not prev_throw:
        print(f"Error: Previous throw with id {last_throw_id} not found.")
        return

    # 6. Restore files to previous throw's file_contents
    prev_files = prev_throw.get("file_contents", {})
    for rel_path, content in prev_files.items():
        abs_path = os.path.join(project_path, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 7. Delete files not present in previous throw
    # Build set of all files in prev_files
    prev_file_set = set(prev_files.keys())
    # Walk project dir (excluding .pebble and ignored files)
    ignore_files = set()
    for ignore_name in [".pebbleignore", "pebbleignore"]:
        ignore_path = os.path.join(project_path, ignore_name)
        if os.path.isfile(ignore_path):
            with open(ignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        ignore_files.add(line)
    for root, dirs, files in os.walk(project_path):
        if ".pebble" in dirs:
            dirs.remove(".pebble")
        for file in files:
            rel_dir = os.path.relpath(root, project_path)
            rel_file = os.path.join(rel_dir, file) if rel_dir != "." else file
            if rel_file in ignore_files or file in ignore_files:
                continue
            if rel_file not in prev_file_set:
                abs_path = os.path.join(root, file)
                try:
                    os.remove(abs_path)
                except Exception:
                    pass

    # 8. Update project_info.json (head_commit, file_hashes)
    db = TinyDB(info_path)
    if len(db) > 0:
        file_hashes = {}
        import hashlib
        for rel_path, content in prev_files.items():
            hasher = hashlib.sha256()
            hasher.update(content.encode("utf-8"))
            file_hashes[rel_path] = hasher.hexdigest()
        db.update({"head_commit": last_throw_id, "file_hashes": file_hashes})
    db.close()

    print(f"Project reset to previous throw {last_throw_id}.")

def reset_to_head_commit(project_path: str):
    """
    Reset the project to the current head commit by replaying all throws in order.
    """
    pebble_dir = os.path.join(project_path, ".pebble")
    info_path = os.path.join(pebble_dir, "project_info.json")
    throws_path = os.path.join(pebble_dir, "project_throws.json")

    # 1. Validate
    if not validate_project(project_path):
        return

    # 2. Load current head_commit
    db = TinyDB(info_path)
    if len(db) == 0:
        print("Error: project_info.json is empty.")
        db.close()
        return
    info = db.all()[0]
    head_commit = info.get("head_commit")
    db.close()
    if not head_commit:
        print("Error: No head_commit found.")
        return

    # 3. Load all throws and build a map {throw_id: throw}
    db = TinyDB(throws_path)
    throws = db.all()
    db.close()
    throw_map = {t.get("throw_id"): t for t in throws}

    # 4. Build the chain of throws from the first to head_commit
    chain = []
    # Find the root throw (no last_throw_id or last_throw_id not in throw_map)
    root = None
    for t in throws:
        if not t.get("last_throw_id") or t.get("last_throw_id") not in throw_map:
            root = t
            break
    if not root:
        print("Error: Could not find root throw.")
        return
    # Walk the chain
    current = root
    while current:
        chain.append(current)
        if current.get("throw_id") == head_commit:
            break
        # Find next throw in chain
        next_throw = None
        for t in throws:
            if t.get("last_throw_id") == current.get("throw_id"):
                next_throw = t
                break
        current = next_throw
    else:
        print("Error: Could not reach head_commit in throw chain.")
        return

    # 5. Replay throws to reconstruct file state
    file_state = {}
    for t in chain:
        # Apply deleted
        for d in t.get("files_changed", {}).get("deleted", []):
            if d in file_state:
                del file_state[d]
        # Apply added/modified
        for k, v in t.get("file_contents", {}).items():
            file_state[k] = v

    # 6. Restore files to reconstructed state
    for rel_path, content in file_state.items():
        abs_path = os.path.join(project_path, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 7. Delete files not present in reconstructed state
    prev_file_set = set(file_state.keys())
    ignore_files = set()
    for ignore_name in [".pebbleignore", "pebbleignore"]:
        ignore_path = os.path.join(project_path, ignore_name)
        if os.path.isfile(ignore_path):
            with open(ignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        ignore_files.add(line)
    for root, dirs, files in os.walk(project_path):
        if ".pebble" in dirs:
            dirs.remove(".pebble")
        for file in files:
            rel_dir = os.path.relpath(root, project_path)
            rel_file = os.path.join(rel_dir, file) if rel_dir != "." else file
            if rel_file in ignore_files or file in ignore_files:
                continue
            if rel_file not in prev_file_set:
                abs_path = os.path.join(root, file)
                try:
                    os.remove(abs_path)
                except Exception:
                    pass

    # 8. Update project_info.json (head_commit, file_hashes)
    db = TinyDB(info_path)
    if len(db) > 0:
        file_hashes = {}
        import hashlib
        for rel_path, content in file_state.items():
            hasher = hashlib.sha256()
            hasher.update(content.encode("utf-8"))
            file_hashes[rel_path] = hasher.hexdigest()
        db.update({"head_commit": head_commit, "file_hashes": file_hashes})
    db.close()

    print(f"Project reset to head commit {head_commit}.")
