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
