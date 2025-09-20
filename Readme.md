# Pebbles VCS

_A simple, offline version control system (like Git, but intentionally minimal and local only)._

---

## 🚀 Core Commands

| Command         | Description                     |
| --------------- | ------------------------------- |
| `pebble init`   | Start a new project             |
| `pebble gather` | Stage files (detect changes)    |
| `pebble throw`  | Commit staged changes           |
| `pebble reset`  | Undo last throw                 |
| `pebble delete` | Remove a project from Pebbles   |
| `pebble clone`  | Copy an existing Pebble project |

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

Restores the project to the exact state of the current head commit by replaying all throws from the beginning.

**How it works:**

1. Loads all throws from `.pebble/project_throws.json` and the current head commit from `.pebble/project_info.json`.
2. Replays each throw in order, applying all additions, modifications, and deletions, to reconstruct the full project state at the head commit.
3. Restores all files in the working directory to match the reconstructed state, and deletes any files that should not exist (unless ignored).
4. Updates `.pebble/project_info.json` to set the head and file hashes to match the reconstructed state.

**Function:**

```python
reset_to_head_commit(project_path)
```

**CLI:**

```bash
pebble reset
```

---

## 🗑️ `delete` — Remove a Project

Securely removes a project from the Pebbles database and your local machine.

**How it works:**

1. Asks for confirmation twice (`YES` required both times).
2. Reads the project name from `.pebble/project_info.json` in the project directory.
3. Deletes the corresponding info file from the main Pebbles folder (e.g., `{project_name}_info.json`).
4. Deletes the `.pebble` directory in the project folder.
5. Prints status messages for each step.

**Function:**

```python
delete_project(project_path)
```

**CLI:**

```bash
pebble delete
```

---

## 🟣 `clone` — Copy an Existing Project

Creates a new, independent project by reconstructing the state of another project at its head commit.

**How it works:**

1. Asks for the project name to clone.
2. Looks up the project location in `{project_name}_info.json` in the main Pebbles folder.
3. Reads the `.pebble/project_info.json` and `.pebble/project_throws.json` from the source project.
4. Replays all throws in order to reconstruct the full project state at the head commit.
5. Writes the reconstructed files to the destination directory (no `.pebble` folder is copied).
6. The result is a new, independent project directory with the same files as the original at its latest commit, but with no version history or metadata.

**Function:**

```python
clone_project(project_name, destination_path, main_pebbles_path)
```

**CLI:**

```bash
pebble clone "project-name" "destination-path"
```

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
