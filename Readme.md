# Pebbles VCS

_A simple, offline version control system (like Git, but intentionally minimal and local only)._

---

## 🚀 Core Commands

| Command           | Description                                 |
|-------------------|---------------------------------------------|
| `pebble init`     | Start a new project                         |
| `pebble gather`   | Stage files (detect changes)                |
| `pebble throw`    | Commit staged changes                       |
| `pebble reset`    | Undo last throw                             |
| `pebble delete`   | Remove a project from Pebbles               |
| `pebble clone`    | Copy an existing Pebble project             |

---

## 📁 Project Structure

**Main Pebbles folder** (for info and easier cloning):

- Project folder location (full path)
- Head commit (current throw)
- Description

**Throw ID:** 10-digit randomly generated (unique per commit)

**Project names must be unique!**

---

## 🟢 `init` — Initialize a Project

Creates a `.pebble` folder in your project directory and registers the project in the main Pebbles folder.

**Creates:**
- `.pebble/project_info.json` — Project metadata
- `.pebble/project_throws.json` — All throws (commits)
- `.pebble/track.json` — Staged files

**Example project_info.json:**
```json
{
  "project_name": "MyProject",
  "date": "2025-09-15",
  "head_commit": null,
  "file_hashes": {},
  "desc": ""
}
```

**Function:**
```python
init(project_path, main_pebbles_folder_path, project_name, desc="")
```

**CLI:**
```bash
pebble init "project-name" -d "Description (Optional)"
```

---

## 🟡 `gather` — Stage/Detect Changes

Scans the project directory for changes and categorizes files as Added, Modified, or Deleted. Updates `.pebble/track.json` accordingly.

**Function:**
```python
gather(project_path, folders_list=[])
```

**CLI:**
```bash
pebble gather .
```

---

## 🟠 `throw` — Commit Staged Changes

Creates a new throw (commit) with a unique throw ID, saves file contents, and updates project metadata.

**Function:**
```python
throw(project_path, pebbles_path, message="")
```

**CLI:**
```bash
pebble throw -m "Commit message"
```

---

## 🟤 `reset` — Undo Last Throw

Reverts the project to the previous throw (commit).

**How it works:**
1. Loads the current head throw from `.pebble/project_info.json`.
2. Finds the previous throw using `last_throw_id` in `.pebble/project_throws.json`.
3. Restores all files to the state of the previous throw.
4. Updates `.pebble/project_info.json` to set the new head and file hashes.

**Function:**
```python
reset(project_path)
```

**CLI:**
```bash
pebble reset
```

---

## 🗑️ `delete` — Remove a Project

Removes a project from the Pebbles database. (Details: TODO)

---

## 🧩 Data File Examples

**project_info.json**
```json
{
  "project_name": "MyProject",
  "date": "2025-09-15",
  "head_commit": "abc123def4",
  "file_hashes": {
    "src/main.py": "a1b2c3..."
  },
  "desc": "A sample project."
}
```

**project_throws.json**
```json
{
  "throw_id": "abc123def4",
  "last_throw_id": "xyz987uvw0",
  "files_changed": {
    "added": ["src/main.py"],
    "modified": [],
    "deleted": []
  },
  "file_contents": {
    "src/main.py": "print('Hello World')"
  },
  "timestamp": "2025-09-15T12:34:56",
  "commit_message": "Initial commit"
}
```

**track.json**
```json
{
  "added": ["src/main.py"],
  "modified": [],
  "deleted": []
}
```

---

## 📝 Notes

- `.pebble` folder is never versioned or restored.
- Untracked files are ignored during reset.
- Always commit (throw) before resetting to avoid losing uncommitted changes.

---

## 📚 Roadmap / TODO

- [ ] CLI for all commands
- [ ] More robust error handling
- [ ] Add branching/merging (maybe)
- [ ] Improve documentation