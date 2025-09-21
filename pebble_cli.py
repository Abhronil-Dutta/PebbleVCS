import argparse
import sys
import os

from init import init
from gather import gather
from throw import throw
from reset import reset
from delete import delete_project
from clone import clone_project
from dotenv import load_dotenv

def main():
    parser = argparse.ArgumentParser(
        description="Pebbles VCS - A minimal, local version control system."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # init
    p_init = subparsers.add_parser(
        "init",
        help="Initialize a new Pebble project",
        description="Initialize a new Pebble project.\n\nSyntax: pebble init [project_path] [-d \"Description\"]"
    )
    p_init.add_argument("project_path", nargs="?", default=os.getcwd(), help="Path to project folder (default: current directory)")
    p_init.add_argument("-d", "--desc", default="", help="Project description")

    # gather
    p_gather = subparsers.add_parser(
        "gather",
        help="Stage/detect changes",
        description="Stage/detect changes in the project.\n\nSyntax: pebble gather [project_path] [folders ...]"
    )
    p_gather.add_argument("project_path", nargs="?", default=os.getcwd(), help="Path to project folder (default: current directory)")
    p_gather.add_argument("folders", nargs="*", help="Folders to scan (optional)")

    # throw
    p_throw = subparsers.add_parser(
        "throw",
        help="Commit staged changes",
        description="Commit staged changes.\n\nSyntax: pebble throw [project_path] -m \"Commit message\""
    )
    p_throw.add_argument("project_path", nargs="?", default=os.getcwd(), help="Path to project folder (default: current directory)")
    p_throw.add_argument("-m", "--message", default="", help="Commit message")

    # reset
    p_reset = subparsers.add_parser(
        "reset",
        help="Undo last throw",
        description="Undo last throw (revert to previous commit).\n\nSyntax: pebble reset [project_path]"
    )
    p_reset.add_argument("project_path", nargs="?", default=os.getcwd(), help="Path to project folder (default: current directory)")

    # delete
    p_delete = subparsers.add_parser(
        "delete",
        help="Delete a Pebble project",
        description="Delete a Pebble project.\n\nSyntax: pebble delete [project_path]"
    )
    p_delete.add_argument("project_path", nargs="?", default=os.getcwd(), help="Path to project folder (default: current directory)")

    # clone (still requires explicit paths)
    p_clone = subparsers.add_parser(
        "clone",
        help="Clone a Pebble project",
        description="Clone a Pebble project.\n\nSyntax: pebble clone <project_name> <destination_path>"
    )
    p_clone.add_argument("project_name", help="Name of project to clone")
    p_clone.add_argument("destination_path", help="Destination folder path")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    load_dotenv()
    MAIN_PEBBLES_PATH = os.getenv("MAIN_PEBBLES_PATH")

    if args.command == "init":
        init(args.project_path, MAIN_PEBBLES_PATH, args.project_path, desc=args.desc)
    elif args.command == "gather":
        gather(args.project_path, args.folders)
    elif args.command == "throw":
        throw(args.project_path, args.message)
    elif args.command == "reset":
        reset(args.project_path)
    elif args.command == "delete":
        delete_project(args.project_path, MAIN_PEBBLES_PATH)
    elif args.command == "clone":
        clone_project(args.project_name, args.destination_path, MAIN_PEBBLES_PATH)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
