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
        create_project_throws_file(project_path)
            - Empty TinyDB file for all commits (“throws”).
        create_project_track_file(project_path)
            - Empty TinyDB file for tracking staged files.

    4. File Hashing + Initial State
        scan_project_files(project_path)
            - Walk through all files (excluding .pebble).
            - Generate hashes.
            - Return dict: { "file-path": "hash" }.
        store_initial_file_state(project_path, file_hashes)
            - Save this into project-info.json (TinyDB doc).
            - head = null initially.

    5. Confirmation
        print_init_success(project_name, project_path)
            - User feedback -> "Pebble successfully initiated!!"
            - Any Error -> "Unasble to initiate Pebble: <error message>"
"""


def check_project_exists(project_name, main_pebbles_path) -> bool:
    """
    Check if a project with the given name already exists in the main Pebbles database.
    
    Args:
        project_name (str): The name of the project to check.
        main_pebbles_path (str): The path to the main Pebbles database (TinyDB or JSON).
    
    Returns:
        bool: True if the project exists, False otherwise.
    """
    # Implementation goes here
    return False  # Placeholder return value


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
    # Implementation goes here
    return True  # Placeholder return value


def create_pebble_folder(project_path) -> bool:
    """
    Create a .pebble directory inside the project root.
    
    Args:
        project_path (str): The full path to the project folder.
    
    Returns:
        bool: True if registration was successful, False otherwise.
    """
    # Implementation goes here
    return True  # Placeholder return value

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
    # Implementation goes here
    return True  # Placeholder return value

def create_project_throws_file(project_path) -> bool:
    """
    Create an empty TinyDB file for all commits ("throws") inside the .pebble directory.
    
    Args:
        project_path (str): The full path to the project folder.
    
    Returns:
        bool: True if the file was created successfully, False otherwise.
    """
    # Implementation goes here
    return True  # Placeholder return value

def create_project_track_file(project_path) -> bool:
    """
    Create an empty TinyDB file for tracking staged files inside the .pebble directory.
    
    Args:
        project_path (str): The full path to the project folder.
    
    Returns:
        bool: True if the file was created successfully, False otherwise.
    """
    # Implementation goes here
    return True  # Placeholder return value

def scan_project_files(project_path) -> dict:
    """
    Scan all files in the project directory (excluding .pebble and the files listed in .pebbleignore/pebbleignore) and generate their hashes.
    
    Args:
        project_path (str): The full path to the project folder.
    
    Returns:
        dict: A dictionary mapping file paths to their hashes.
    """
    # Implementation goes here
    return {}  # Placeholder return value

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

def print_init_success(project_name, project_path):
    """
    Print a success message after initializing the Pebble project.
    
    Args:
        project_name (str): The name of the project.
        project_path (str): The full path to the project folder.
    """
    print(f"Pebble successfully initiated for project '{project_name}' at '{project_path}'!")

def print_init_error(error_message):
    """
    Print an error message if the Pebble project initialization fails.
    
    Args:
        error_message (str): The error message to display.
    """
    print(f"Unable to initiate Pebble: {error_message}")