"""
    1) Generate a throw id of 10 characters
        - Use a secure random generator to create a unique identifier for the throw.
    2) Check if the throw id already exists
        - Look in the {project_name}_throws.json file in the .pebble directory for an entry with the same throw id.
        - If it exists, generate a new throw id and check again.
        - Ensures unique throw ids.
    2) Checks tracked files
        - Look in track.json in the .pebble directory for files that are staged for commit.
        - If no files are staged, raise an error and exit.
    3) Scan project files
        - Scan the project directory (excluding the .pebble folder) to get the current state of files.
        - Scan the texts of the files and store them in dictionary
    4) Make a throw object
        - throw id : 
        - last throw id :
        - files changed :
             - added : dict of added files and their hashes
             - modified : dict of modified files and their hashes
                - deleted : list of deleted file paths
        - content of files : dict of file paths and their texts
        - timestamp : current date and time
        - commit message : user provided message
    5) Store the throw object
        - Append the throw object to the {project_name}_throws.json file in the .pebble directory.
        - Update the project info file with the new head commit and file hashes.
    6) Clear the track file
        - Empty the track.json file in the .pebble directory.
    7) Update the main Pebbles database
        - Update the head commit for the project in the main Pebbles database.
    8) Confirmation
        - Print a success message with the throw id.
        - Any Error -> "Unable to create throw: <error message>"
    
"""

from typing import Dict
from tinydb import TinyDB
import os
import json

from gather import _load_project_info

def generate_throw_id(length=10) -> str:
    """Generate a secure random throw id of specified length."""
    import secrets
    import string
    alphabet = string.ascii_letters + string.digits
    id = ''.join(secrets.choice(alphabet) for _ in range(length))
    return id

def check_throw_id_exists(throw_id: str, project_path: str) -> bool:
    """Check if a throw id already exists in the throws database."""
    throws_path = os.path.join(project_path, ".pebble", "project_throws.json")
    db = TinyDB(throws_path)
    exists = any(entry.get("throw_id") == throw_id for entry in db.all())
    db.close()
    return exists

def check_tracked_files(project_path: str) -> list:
    """Check the track file for staged files."""
    track_path = os.path.join(project_path, ".pebble", "track.json")
    db = TinyDB(track_path)
    tracked_files = []
    for entry in db.all():
        # Accept both dict and list formats
        if isinstance(entry, dict):
            for key in ["Added", "Modified"]:
                if key in entry:
                    tracked_files.extend(entry[key])
        elif isinstance(entry, list):
            tracked_files.extend(entry)
    db.close()
    return tracked_files

def check_tracked_files_and_deleted(project_path: str):
    """Check the track file for staged files and deleted files."""
    track_path = os.path.join(project_path, ".pebble", "track.json")
    db = TinyDB(track_path)
    added = []
    modified = []
    deleted = []
    for entry in db.all():
        if isinstance(entry, dict):
            if "Added" in entry:
                added.extend(entry["Added"])
            if "Modified" in entry:
                modified.extend(entry["Modified"])
            if "Deleted" in entry:
                deleted.extend(entry["Deleted"])
    db.close()
    return added, modified, deleted

def scan_project_files(project_path: str, folders_list: list) -> Dict[str, str]:
    """Scan only the files listed in folders_list (which are the tracked files). Ignores files in .pebbleignore/pebbleignore."""
    file_contents = {}
    ignore_files = set()
    for ignore_name in [".pebbleignore", "pebbleignore"]:
        ignore_path = os.path.join(project_path, ignore_name)
        if os.path.isfile(ignore_path):
            with open(ignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        ignore_files.add(line)
    for rel_path in folders_list:
        # rel_path is relative to project_path
        if rel_path in ignore_files or os.path.basename(rel_path) in ignore_files:
            continue
        abs_path = os.path.join(project_path, rel_path)
        if not os.path.isfile(abs_path):
            continue
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                file_contents[rel_path] = f.read()
        except (UnicodeDecodeError, OSError):
            continue
    return file_contents

def create_throw_object(throw_id: str, last_throw_id: str, files_changed: Dict[str, Dict], file_contents: Dict[str, str], commit_message: str) -> Dict:
    """Create a throw object with the specified details."""
    from datetime import datetime
    throw = {
        "throw_id": throw_id,
        "last_throw_id": last_throw_id,
        "files_changed": files_changed,
        # Only include file_contents for added/modified, not for deleted
        "file_contents": {k: v for k, v in file_contents.items() if k not in files_changed.get("deleted", [])},
        "timestamp": datetime.now().isoformat(),
        "commit_message": commit_message
    }
    return throw

def store_throw_object(throw: Dict, project_path: str):
    """Store the throw object in the throws database."""
    throws_path = os.path.join(project_path, ".pebble", "project_throws.json")
    db = TinyDB(throws_path)
    db.insert(throw)
    db.close()

def clear_track_file(project_path: str):
    """Clear the track file."""
    track_path = os.path.join(project_path, ".pebble", "track.json")
    db = TinyDB(track_path)
    db.truncate()
    db.close()

def update_project_info(project_path: str, new_head_commit: str, new_file_hashes: Dict[str, str], main_pebbles_path: str, project_name: str, added=None, modified=None, deleted=None):
    """Update the project info file and the main Pebbles database."""
    pebble_dir = os.path.join(project_path, ".pebble")
    info_path = os.path.join(pebble_dir, "project_info.json")
    # Update project info file
    db = TinyDB(info_path)
    if len(db) > 0:
        info = db.all()[0]
        file_hashes = info.get("file_hashes", {})
        # Update only added/modified
        if added:
            for k, v in added.items():
                file_hashes[k] = v
        if modified:
            for k, v in modified.items():
                file_hashes[k] = v
        # Remove deleted
        if deleted:
            for k in deleted:
                if k in file_hashes:
                    del file_hashes[k]
        db.update({"head_commit": new_head_commit, "file_hashes": file_hashes})
    db.close()
    # Update main Pebbles database: open the correct {project_name}_info.json file and update head_commit
    main_db_path = os.path.join(main_pebbles_path, f"{project_name}_info.json")
    if os.path.isfile(main_db_path):
        main_db = TinyDB(main_db_path)
        # TinyDB default table is '_default', doc_id starts at 1
        main_db.table('_default').update({"head_commit": new_head_commit}, doc_ids=[1])
        main_db.close()

def confirmation_message(throw_id: str):
    """Print a success message with the throw id."""
    print(f"Throw created successfully with ID: {throw_id}")

def throw(project_path: str, commit_message: str, folders_list: list = [], main_pebbles_path: str = "E:\\Projects\\Pebbles"):
    try:
        project_path = os.path.abspath(project_path)
        pebble_dir = os.path.join(project_path, ".pebble")
        if not os.path.isdir(pebble_dir):
            raise Exception(".pebble folder not found in project path")
        info_path = os.path.join(pebble_dir, "project_info.json")
        if not os.path.isfile(info_path):
            raise Exception("No project info file found in .pebble folder")
        # Load project_name from info file
        db = TinyDB(info_path)
        if len(db) == 0:
            db.close()
            raise Exception("Project info file is empty")
        info = db.all()[0]
        project_name = info.get("project_name", "")
        last_head_commit = info.get("head_commit", "")
        db.close()

        # Step 1: Generate a throw id
        throw_id = generate_throw_id()

        # Step 2: Check if the throw id already exists
        while check_throw_id_exists(throw_id, project_path):
            throw_id = generate_throw_id()

        # Step 3: Check tracked files and deleted files
        added_files, modified_files, deleted_files = check_tracked_files_and_deleted(project_path)
        if not (added_files or modified_files or deleted_files):
            raise Exception("No files are staged for commit.")

        # Step 4: Scan only tracked files, ignore .pebbleignore
        file_contents = scan_project_files(project_path, added_files + modified_files)

        # Compute hashes for tracked files
        import hashlib
        def file_hash(path):
            abs_path = os.path.join(project_path, path)
            hasher = hashlib.sha256()
            try:
                with open(abs_path, 'rb') as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        hasher.update(chunk)
                return hasher.hexdigest()
            except Exception:
                return ""

        current_file_hashes = {path: file_hash(path) for path in (added_files + modified_files) if os.path.isfile(os.path.join(project_path, path))}

        # Determine added, modified, deleted files
        baseline = _load_project_info(project_path, project_name)
        prev_file_hashes = baseline["file_hashes"]
        added = {path: current_file_hashes[path] for path in added_files if path not in prev_file_hashes}
        modified = {path: current_file_hashes[path] for path in modified_files if path in prev_file_hashes and prev_file_hashes[path] != current_file_hashes[path]}
        deleted = deleted_files
        files_changed = {
            "added": added,
            "modified": modified,
            "deleted": deleted
        }

        # Step 5: Make a throw object (store file contents only in throw)
        throw_obj = create_throw_object(throw_id, last_head_commit, files_changed, file_contents, commit_message)

        # Step 6: Store the throw object
        store_throw_object(throw_obj, project_path)

        # Step 7: Clear the track file
        clear_track_file(project_path)
        # Step 8: Update the project info file and main Pebbles database (only hashes)
        new_head_commit = throw_id
        update_project_info(
            project_path,
            new_head_commit,
            current_file_hashes,
            main_pebbles_path,
            project_name,
            added=added,
            modified=modified,
            deleted=deleted
        )
        # Step 9: Confirmation
        confirmation_message(throw_id)
    except Exception as e:
        print(f"Unable to create throw: {str(e)}")
