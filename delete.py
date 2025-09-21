"""
It asks the user for confirmation twice (YES required both times).
It reads the project name from .pebble/project_info.json.
It deletes the corresponding info file from the main Pebbles folder.
It deletes the .pebble directory in the project.
It prints status messages for each step.

"""

import os
import shutil
from tinydb import TinyDB
from dotenv import load_dotenv

load_dotenv()

MAIN_PEBBLES_PATH = os.getenv("MAIN_PEBBLES_PATH")

def delete_project(project_path: str, main_pebbles_path: str = None):
    if main_pebbles_path is None:
        main_pebbles_path = MAIN_PEBBLES_PATH
    # Double confirmation
    confirm1 = input("Are you sure? (YES/no): ")
    if confirm1.strip() != "YES":
        print("Aborted.")
        return
    confirm2 = input("Are you REALLY sure? (YES/no): ")
    if confirm2.strip() != "YES":
        print("Aborted.")
        return
    pebble_dir = os.path.join(project_path, ".pebble")
    info_path = os.path.join(pebble_dir, "project_info.json")
    if not os.path.isfile(info_path):
        print("project_info.json not found in .pebble directory.")
        return
    db = TinyDB(info_path)
    if len(db) == 0:
        print("project_info.json is empty.")
        db.close()
        return
    info = db.all()[0]
    project_name = info.get("project_name")
    db.close()
    if not project_name:
        print("Project name not found in project_info.json.")
        return
    # Delete info file from main Pebbles folder
    main_info_path = os.path.join(main_pebbles_path, f"{project_name}_info.json")
    if os.path.isfile(main_info_path):
        os.remove(main_info_path)
        print(f"Deleted {main_info_path}")
    else:
        print(f"Info file {main_info_path} not found in main Pebbles folder.")
    # Delete .pebble directory
    if os.path.isdir(pebble_dir):
        shutil.rmtree(pebble_dir)
        print(f"Deleted {pebble_dir}")
    else:
        print(f".pebble directory not found at {pebble_dir}.")
    print("Project deleted.")

