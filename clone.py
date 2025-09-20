import os
import shutil
from tinydb import TinyDB

def clone_project(project_name: str, destination_path: str, main_pebbles_path: str):
    # Find info file in main Pebbles folder
    info_path = os.path.join(main_pebbles_path, f"{project_name}_info.json")
    if not os.path.isfile(info_path):
        print(f"Project info file {info_path} not found.")
        return
    db = TinyDB(info_path)
    if len(db) == 0:
        print("Project info file is empty.")
        db.close()
        return
    info = db.all()[0]
    folder_location = info.get("folder_location")
    db.close()
    if not folder_location or not os.path.isdir(folder_location):
        print(f"Project folder {folder_location} not found.")
        return
    pebble_dir = os.path.join(folder_location, ".pebble")
    if not os.path.isdir(pebble_dir):
        print(f".pebble directory not found in {folder_location}.")
        return
    # Prepare destination
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    # Load throws and info from source .pebble
    info_src = os.path.join(pebble_dir, "project_info.json")
    throws_src = os.path.join(pebble_dir, "project_throws.json")
    # Read head_commit
    db = TinyDB(info_src)
    info_data = db.all()[0]
    head_commit = info_data.get("head_commit")
    db.close()
    # Read all throws
    db = TinyDB(throws_src)
    throws = db.all()
    db.close()
    throw_map = {t.get("throw_id"): t for t in throws}
    # Build throw chain
    chain = []
    root = None
    for t in throws:
        if not t.get("last_throw_id") or t.get("last_throw_id") not in throw_map:
            root = t
            break
    if not root:
        print("Error: Could not find root throw.")
        return
    current = root
    while current:
        chain.append(current)
        if current.get("throw_id") == head_commit:
            break
        next_throw = None
        for t in throws:
            if t.get("last_throw_id") == current.get("throw_id"):
                next_throw = t
                break
        current = next_throw
    else:
        print("Error: Could not reach head_commit in throw chain.")
        return
    # Replay throws to reconstruct file state
    file_state = {}
    for t in chain:
        for d in t.get("files_changed", {}).get("deleted", []):
            if d in file_state:
                del file_state[d]
        for k, v in t.get("file_contents", {}).items():
            file_state[k] = v
    # Write files to destination (no .pebble)
    for rel_path, content in file_state.items():
        abs_path = os.path.join(destination_path, rel_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"Project '{project_name}' cloned to {destination_path} as a new independent project.")

clone_project("ai", "E:/Projects/ai_clone", "E:/Projects/Pebbles")