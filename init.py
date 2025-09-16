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

    4. Confirmation
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
    file_name = "project_info.json"  # Changed from f"{project_name}_info.json"
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
    file_name = "project_throws.json"  # Changed from f"{project_name}_throws.json"
    file_path = os.path.join(project_path, ".pebble", file_name)
    try:
        db = TinyDB(file_path)
        db.close()  # Create an empty file
        return True
    except Exception as e:
        print(f"Error creating project throws file: {e}")
        return False

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
# Main function to initialize a new Pebble project
#----------------------------------------------------------------------------------------------------------

def init(project_name, project_path, desc="") -> bool:
    """
    Initialize a new Pebble project.
    
    Args:
        project_name (str): The name of the project.
        project_path (str): The full path to the project folder.
        desc (str): A description of the project (optional).
    
    Returns:
        bool: True if initialization was successful, False otherwise.
    """
    if check_project_exists(project_name, main_pebbles_path):
        print_init_error(f"Project '{project_name}' already exists.")
        return False
    
    if not register_project_in_main(project_name, project_path, main_pebbles_path, desc):
        print_init_error("Failed to register project in main Pebbles database.")
        return False
    
    if not create_pebble_folder(project_path):
        print_init_error("Failed to create .pebble directory.")
        return False
    
    if not create_project_info_file(project_path, project_name, desc):
        print_init_error("Failed to create project info file.")
        return False
    
    if not create_project_throws_file(project_path, project_name):
        print_init_error("Failed to create project throws file.")
        return False
    
    if not create_project_track_file(project_path):
        print_init_error("Failed to create project track file.")
        return False
    
    print_init_success(project_name, project_path)
    return True

#----------------------------------------------------------------------------------------------------------

init("TestProject", "E:\C and C++", "This is a test project.")