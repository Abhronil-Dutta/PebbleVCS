# Pebbles

_(Like Git but offline and worse)_

## Core Commands

- pebble init - Start a new project
- pebble clone - Copy an existing Pebble project

---

- pebble gather - Stage files
- pebble throw - Commit staged changes

---

- pebble pickup - Restore a previous throw (checkout-ish)
- pebble reset - Undo last throw

---

- pebble delete - Remove a project from Pebbles

---

### Main folder

Pebbles folder -> Project older (For info puposes.. makes it easier to clone) <br>
-> folder location on local computer <br>
-> Head commit <br>

### **Throw ID** - 10 digit ramdomly generated

**Project Name needs to be unique**

## **init**

- Project name
- Date
- Head
- no. of commits (Later on)
- files and their hashes
- files contents
- tracked files states

---

**The init function does these following things**

- Creates a .pebble folder in the project dir
- Creates a {project_name}\_info in the main **Pebbles** folder (not in the dir)

```json
{
  "folder_location(full)": "E:/Whatever",
  "head_commit": null,
  "desc": ""
}
```

- Creates 3 json files in the .pebble folder
  - _project-info_
  ```json
  {
      "name": "Project name (must be unique)",
      "date" : "",
      "head" : null (initially null later will update),
      "file-hashes" : {
          "file-path" : "file hash"
      },
      "desc" : ""
  }
  ```
  - _project-throws_
  ```json
  {
    "throw-id": 1234567890,
    "last-throw-id": 0987654321,
    "files-changed": {
      "Added": [],
      "Modified": [],
      "Deleted": []
    },
    "contents": { "file-path/name": "Full Content print('Hello World')" },
    "throw-msg": "It's over Anakin! I have the high ground!"
  }
  ```
  - _project-track_
  ```json
  {
    "last commit": 0987654321,
    "Added": [],
    "Modified": [],
    "Deleted": []
  }
  ```

---

### Function Structure

```py
init(project_path, main_pebbles_folder_path,project_name, desc=""):

    if project_exists(project_name, main_pebbles_path):
        print("Please choose a unique name for your project!")
        return

    try:
        # Create .pebble folder + json files
        # Register project in Pebbles folder
        print("Pebble successfully innitiated!!")
    except Exception as e:
        print("Unable to innitialise pebble project", e)
```

### CLI (TODO)

project path -> From where the cmd is ran
main pebbles folder path -> fixed path (e.g., in C:/Pebbles/)
So final command :-

```bash
pebbles init "project-name" -d "Description (Optional)"
```

## gather

checks the whole project directory and checks the changed files. then categorises them into added, modified and deleted.

### Function Structure

```py
gather(project_path, folders_list = [])
```

### Parameters:

- project_path (str): Path to the root of the project.
- folders_list (list, optional): List of specific folders to scan. If empty, the entire project is scanned.

Scans the files in the project_path. <br>
It has 3 categories to put files in

- Added
- Modified
- Deleted

Scans and generates hashes for the files, sets them in a directory then compares with file_hashes in {project_info} <br>

- If a file is in project-info and not in dictionary.. its categorized as added
- If a file is in project-info and in dictionary but their hashes are different.. its categorized as modified
- If a file is in project-info but not in dictionary.. its categorized as deleted (only add deleted if folders_list is empty i.e. scans the whole project)

then take the head from the 'project_info'
and add the track to track.json using tinydb

### CLI (TODO)

project path -> from where the cmd is ran,
. -> for all files
specific file path separated by space

```bash
pebbles gather .
```
