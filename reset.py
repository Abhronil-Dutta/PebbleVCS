"""
    Reset (undo last throw) functionality.

    1) Validate project and .pebble files exist.
    2) Load current head_commit from project_info.json.
    3) Find the current throw in project_throws.json.
    4) Get last_throw_id from current throw.
    5) Find the previous throw object.
    6) Restore files to previous throw's file_contents.
    7) Delete files not present in previous throw.
    8) Update project_info.json (head_commit, file_hashes).
    9) Print confirmation.
"""