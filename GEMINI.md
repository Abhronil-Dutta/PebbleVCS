# Project Overview

This project is "PebbleVCS," a minimal, local-only version control system written in Python. It is designed as a simple alternative to systems like Git, intended for projects that do not require remote repositories or complex branching and merging.

The core functionalities include:
- `init`: Initializes a new versioned project.
- `gather`: Stages changes by detecting added, modified, or deleted files.
- `throw`: Commits the staged changes.
- `reset`: Reverts the project to the last commit.
- `clone`: Creates a copy of a project's latest state.
- `delete`: Removes a project from PebbleVCS tracking.

The system relies on a central folder defined by the `MAIN_PEBBLES_PATH` environment variable to store metadata about all tracked projects. Each project folder contains a hidden `.pebble` directory with its specific history and tracking information, managed through JSON files using the `tinydb` library.

# Building and Running

## Dependencies
The project's dependencies are listed in `requirements.txt`. To install them, run:
```bash
pip install -r requirements.txt
```

## Environment Setup
PebbleVCS requires a `MAIN_PEBBLES_PATH` environment variable to be set. This variable should point to the directory where PebbleVCS will store its central project tracking files.

Create a `.env` file in the project root with the following content:
```
MAIN_PEBBLES_PATH="C:\path\to\your\pebbles\folder"
```
Replace the path with the desired location on your system.

## Running Commands
The main entry point for the application is `pebble_cli.py`. Commands are run using the following structure:

```bash
python pebble_cli.py <command> [options]
```

**Examples:**
- Initialize a project in the current directory:
  ```bash
  python pebble_cli.py init . -d "My new project"
  ```
- Stage changes:
  ```bash
  python pebble_cli.py gather .
  ```
- Commit changes:
  ```bash
  python pebble_cli.py throw . -m "My commit message"
  ```

# Development Conventions

- The project is structured with each core command implemented in its own Python module (e.g., `init.py`, `throw.py`).
- The `pebble_cli.py` script serves as the command-line interface, using Python's `argparse` library to parse arguments and call the appropriate functions from the command modules.
- The `dotenv` library is used to manage environment variables, specifically for the `MAIN_PEBBLES_PATH`.
- Data is stored in JSON files, and `tinydb` is used for database operations.
