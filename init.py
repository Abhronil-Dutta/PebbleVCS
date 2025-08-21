"""
    1. Validation Layer
        check_project_exists(project_name, main_pebbles_path)
        - Look in main_pebbles_path (TinyDB or flat JSON) for an entry with the same project name.
        - Return True/False.
        - Ensures unique project names.

    2. Project Registration
        - register_project_in_main(project_name, project_path, main_pebbles_path, desc="")
        - Insert into main Pebbles DB (TinyDB file stored at main_pebbles_path/db.json).
        - Stores metadata:
            - Project name
            - Full folder path
            - head_commit = None
            - Description

    3. Local Project Setup
        create_pebble_folder(project_path)
            - Make .pebble directory inside project root.
        create_project_info_file(project_path, project_name, desc="")
            - TinyDB file inside .pebble (e.g., .pebble/project-info.json).
            - Stores project metadata (date, head commit, desc, file hashes).
        create_project_throws_file(project_path, project_name)
            - Empty TinyDB file for all commits (“throws”).
        create_project_track_file(project_path)
            - Empty TinyDB file for tracking staged files.

    4. File Hashing + Initial State
        scan_project_files(project_path)
            - Walk through all files (excluding .pebble).
            - Exclude files listed in .pebbleignore/pebbleignore.
            - generate_file_hash(file_path)
                - For each file, read its content and generate a SHA-256 hash.
                - return hash string.
            - Return dict: { "file-path": "hash" }.
        store_initial_file_state(project_path, file_hashes)
            - Save this into project-info.json (TinyDB doc).
            - head = null initially.

    5. Confirmation
        print_init_success(project_name, project_path)
            - User feedback -> "Pebble successfully initiated!!"
            - Any Error -> "Unasble to initiate Pebble: <error message>"
"""

# Imports
from dotenv import load_dotenv
import os
import json
import hashlib
from tinydb import TinyDB
from datetime import datetime

# Load environment variables
load_dotenv()
main_pebbles_path = os.getenv("MAIN_PEBBLES_PATH")

#----------------------------------------------------------------------------------------------------------

def check_project_exists(project_name, main_pebbles_path) -> bool:
    """
    Check if a project with the given name already exists in the main Pebbles database.
    
    Args:
        project_name (str): The name of the project to check. 
                            File to look for -> project_name_info.json in the main Pebbles directory.
        main_pebbles_path (str): The path to the main Pebbles database (TinyDB or JSON).
    
    Returns:
        bool: True if the project exists, False otherwise.
    """
    file_name = f"{project_name}_info.json"
    file_path = os.path.join(main_pebbles_path, file_name)
    return os.path.isfile(file_path)

#----------------------------------------------------------------------------------------------------------

def register_project_in_main(project_name, project_path, main_pebbles_path, desc="") -> bool:
    """
    Register a new project in the main Pebbles folder.
    
    Args:
        project_name (str): The name of the project.
        project_path (str): The full path to the project folder.
        main_pebbles_path (str): The path to the main Pebbles database.
        desc (str): A description of the project (optional).
    
    Returns:
        bool: True if registration was successful, False otherwise.
    """
    file_name = f"{project_name}_info.json"
    file_path = os.path.join(main_pebbles_path, file_name)
    try:
        db = TinyDB(file_path)
        db.insert({
            "folder_location": project_path,
            "head_commit": None,
            "desc": desc
        })
        db.close()
        return True
    except Exception as e:
        print(f"Error registering project: {e}")
        return False

#----------------------------------------------------------------------------------------------------------

def create_pebble_folder(project_path) -> bool:
    """
    Create a .pebble directory inside the project root.
    
    Args:
        project_path (str): The full path to the project folder.
    
    Returns:
        bool: True if registration was successful, False otherwise.
    """
    try:
        pebble_dir = os.path.join(project_path, ".pebble")
        os.makedirs(pebble_dir, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating .pebble directory: {e}")
        return False
    
#----------------------------------------------------------------------------------------------------------

def create_project_info_file(project_path, project_name, desc="") -> bool:
    """
    Create a project info file inside the .pebble directory.
    
    Args:
        project_path (str): The full path to the project folder.
        project_name (str): The name of the project.
        desc (str): A description of the project (optional).
    
    Returns:
        bool: True if the file was created successfully, False otherwise.
    """
    file_name = f"{project_name}_info.json"
    file_path = os.path.join(project_path, ".pebble", file_name)
    try:
        db = TinyDB(file_path)
        db.insert({
            "project_name" : project_name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "head_commit": None,
            "file_hashes": {},
            "desc": desc
        })
        db.close()
        return True
    except Exception as e:
        print(f"Error creating project info file: {e}")
        return False

#----------------------------------------------------------------------------------------------------------

def create_project_throws_file(project_path, project_name) -> bool:
    """
    Create an empty TinyDB file for all commits ("throws") inside the .pebble directory.
    
    Args:
        project_path (str): The full path to the project folder.
    
    Returns:
        bool: True if the file was created successfully, False otherwise.
    """
    file_name = f"{project_name}_throws.json"
    file_path = os.path.join(project_path, ".pebble", file_name)
    try:
        db = TinyDB(file_path)
        db.close()  # Create an empty file
        return True
    except Exception as e:
        print(f"Error creating project throws file: {e}")
    return True  # Placeholder return value

#----------------------------------------------------------------------------------------------------------

def create_project_track_file(project_path) -> bool:
    """
    Create an empty TinyDB file for tracking staged files inside the .pebble directory.
    
    Args:
        project_path (str): The full path to the project folder.
    
    Returns:
        bool: True if the file was created successfully, False otherwise.
    """
    file_name = "track.json"
    file_path = os.path.join(project_path, ".pebble", file_name)
    try:
        db = TinyDB(file_path)
        db.close()  # Create an empty file
        return True
    except Exception as e:
        print(f"Error creating project track file: {e}")
        return False

#----------------------------------------------------------------------------------------------------------

def scan_project_files(project_path) -> dict:
    """
    Scan all files in the project directory (excluding .pebble and the files listed in .pebbleignore/pebbleignore) and generate their hashes.
    
    Args:
        project_path (str): The full path to the project folder.
    
    Returns:
        dict: A dictionary mapping file paths to their hashes.
    """
    
    return {}  # Placeholder return value

#----------------------------------------------------------------------------------------------------------

def generate_file_hash(file_path) -> str:
    """
    Generate a SHA-256 hash for a given file.
    
    Args:
        file_path (str): The path to the file to hash.
    
    Returns:
        str: The SHA-256 hash of the file.
    """
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            # It reads the file in chunks of 8192 bytes (8 KB) at a time. (Better for large files)
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}")
        return ""
    
#----------------------------------------------------------------------------------------------------------

def store_initial_file_state(project_path, file_hashes) -> bool:
    """
    Store the initial file state in the project info file.
    Sets the head commit to None initially.
    
    Args:
        project_path (str): The full path to the project folder.
        file_hashes (dict): A dictionary mapping file paths to their hashes.
    
    Returns:
        bool: True if the initial state was stored successfully, False otherwise.
    """
    # Implementation goes here
    return True  # Placeholder return value

#----------------------------------------------------------------------------------------------------------

def print_init_success(project_name, project_path):
    """
    Print a success message after initializing the Pebble project.
    
    Args:
        project_name (str): The name of the project.
        project_path (str): The full path to the project folder.
    """
    print(f"Pebble successfully initiated for project '{project_name}' at '{project_path}'!")

#----------------------------------------------------------------------------------------------------------

def print_init_error(error_message):
    """
    Print an error message if the Pebble project initialization fails.
    
    Args:
        error_message (str): The error message to display.
    """
    print(f"Unable to initiate Pebble: {error_message}")

#----------------------------------------------------------------------------------------------------------



# Example usage
# project_name = "example_project"
# project_path = "E:/Projects/Pebbles/example_project"
# Description = "This is an example project."
# reg = register_project_in_main(project_name, project_path, main_pebbles_path, Description)
# if reg: 
#     if (check_project_exists(project_name, main_pebbles_path)):
#         print("Project created!")
#     else:
#         print("Project not created!")
# else:
#     print("Failed to register project in main Pebbles database.")

