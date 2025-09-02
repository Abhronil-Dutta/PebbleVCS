"""
1) Normalize Inputs
    - Resolve project_path to an absolute path.
    - Normalize and de-duplicate folders_list (if provided), resolving each to absolute paths within project_path.

2) Load Baseline State
    - Read project_info (where previous file hashes and head live).
    - Extract:
        - prev_hashes: Dict[str, str] (filepath → hash) (Innitailly empty)
        - head: str (latest recorded commit/identifier) (Initially None)

3) Discover Current Files to Scan
    - If folders_list is empty: recursively walk the entire project_path.
    - If folders_list is non-empty: recursively walk only those subpaths.
    - Ignore .pebble and files/directories listed in .pebbleignore.

4) Hash Current Files
    - For each discovered file hash using SHA-256.

5) Compare States (Diff)
    - Initialize three sets/lists: added, modified, deleted.
    - For each path in curr_hashes:
        - If path not in prev_hashes → Added.
        - Else if curr_hashes[path] != prev_hashes[path] → Modified.
    - For Deleted:
        - Only if folders_list is empty (full scan):
        - For each path in prev_hashes not in curr_hashes → Deleted.

6) Assemble Results
    - Create a result object:
    {
        "added": dict of added files and their hashes,
        "modified": dict of modified files and their hashes,
        "deleted": list of deleted file paths,
        "last_commit": head (from project_info),
    }
"""


import hashlib
import os
import json
from tinydb import TinyDB
from typing import List, Dict, Any

"""
    The _normalize_path function takes a path string and converts it to an absolute path.
    For example, it expands user directories (like ~) and resolves relative paths.
    changes ./folder to C:/Project/Name/folder
    Doesnt change absolute paths like C:/Project/Name/folder
"""
def _normalize_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))

"""
    The _load_project_info function reads the project info file from the .pebble directory.
    It returns a dictionary with the previous file hashes and the head commit.
"""
def _load_project_info(project_path: str, project_name: str) -> Dict[str, Any]:
    info_path = os.path.join(project_path, ".pebble", "project_info.json")
    db = TinyDB(info_path)
    if len(db) == 0:
        db.close()
        return {"file_hashes": {}, "head_commit": None}
    info = db.all()[0]
    db.close()
    return {
        "file_hashes": info.get("file_hashes", {}),
        "head_commit": info.get("head_commit", None)
    }

"""
    The _get_ignore_list function reads .pebbleignore or pebbleignore files in the project root.
    It returns a set of file and directory names to ignore during scanning.
"""
def _get_ignore_list(project_path: str) -> set:
    ignore_files = set()
    for ignore_name in [".pebbleignore", "pebbleignore"]:
        ignore_path = os.path.join(project_path, ignore_name)
        if os.path.isfile(ignore_path):
            with open(ignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        ignore_files.add(line)
    return ignore_files


"""
    The _scan_files function walks through the project directory (or specified folders)
    Skips files and directories in the ignore list.
    Returns a dict of relative file paths to their SHA-256 hashes.
"""
def _scan_files(project_path: str, folders_list: List[str]) -> Dict[str, str]:
    file_hashes = {}
    ignore_files = _get_ignore_list(project_path)
    if not folders_list:
        scan_targets = [project_path]
    else:
        scan_targets = []
        for entry in folders_list:
            entry_path = entry if os.path.isabs(entry) else os.path.join(project_path, entry)
            if os.path.isfile(entry_path):
                # Single file
                rel_file = os.path.relpath(entry_path, project_path)
                if rel_file in ignore_files or os.path.basename(entry_path) in ignore_files:
                    continue
                file_hashes[rel_file] = _generate_file_hash(entry_path)
            elif os.path.isdir(entry_path):
                scan_targets.append(entry_path)
    # Walk directories
    for scan_path in scan_targets:
        for root, dirs, files in os.walk(scan_path):
            if ".pebble" in dirs:
                dirs.remove(".pebble")
            for ignore in list(ignore_files):
                if ignore in dirs:
                    dirs.remove(ignore)
            for file in files:
                rel_dir = os.path.relpath(root, project_path)
                rel_file = os.path.join(rel_dir, file) if rel_dir != "." else file
                if rel_file in ignore_files or file in ignore_files:
                    continue
                file_path = os.path.join(root, file)
                file_hashes[rel_file] = _generate_file_hash(file_path)
    return file_hashes

"""
    Helper function to generate SHA-256 hash of a file.
    SHA-256 is chosen for its balance of speed and collision resistance.
"""
def _generate_file_hash(file_path: str) -> str:
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return ""

def gather(project_path: str, folders_list: List[str] = []) -> Dict[str, Any]:
    """
    Scan the project directory and categorize files as added, modified, or deleted.
    Args:
        project_path (str): Path to the root of the project.
        folders_list (list, optional): List of specific folders to scan. If empty, the entire project is scanned.
    Returns:
        dict: Results with added, modified, deleted files and last commit.
    """
    print(project_path)
    project_path = _normalize_path(project_path)
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
    db.close()
    baseline = _load_project_info(project_path, project_name)
    prev_hashes = baseline["file_hashes"]
    head = baseline["head_commit"]
    curr_hashes = _scan_files(project_path, folders_list)
    added = {}
    modified = {}
    deleted = []
    for path, hashval in curr_hashes.items():
        if path not in prev_hashes:
            added[path] = hashval
        elif prev_hashes[path] != hashval:
            modified[path] = hashval
    if not folders_list:
        for path in prev_hashes:
            if path not in curr_hashes:
                deleted.append(path)
    result = {
        "Added": added,
        "Modified": modified,
        "Deleted": deleted,
        "last commit": head
    }
    # Write to track.json in .pebble folder
    track_path = os.path.join(pebble_dir, "track.json")
    db = TinyDB(track_path)
    db.truncate()  # Clear previous tracking info
    db.insert(result)
    db.close()
    # Also return hashes for added/modified for programmatic use
    return {
        "added": added,
        "modified": modified,
        "deleted": deleted,
        "last_commit": head
    }
