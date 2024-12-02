"""
Main module for finding `.tex` files and running ChkTeX on them.

Includes logic to parse files, run ChkTeX, analyze errors, and write a Markdown summary
for GitHub Actions.
"""

import os
import sys
from typing import LiteralString, List, Tuple
from collections import Counter
from chktex import run_chktex, Error
from step_summary import (
    write_step_summary,
    build_markdown_step_summary,
)


def find_tex_files(github_workspace_path: str) -> List[LiteralString | str | bytes]:
    """
    Finds all `.tex` files in the specified GitHub workspace.

    Skips directories like `venv`, `.git`, and `__pycache__`.
    Returns a list of absolute paths for `.tex` files.
    """

    all_files_in_tree = []
    skip_dirs = {"venv", ".git", "__pycache__"}

    for root, dirs, files in os.walk(github_workspace_path, topdown=True):
        for skip_dir in skip_dirs:
            if skip_dir in dirs:
                dirs.remove(skip_dir)

        for file in files:
            all_files_in_tree.append(os.path.join(root, file))

    return [file for file in all_files_in_tree if file.endswith(".tex")]


def analyze_errors(errors: List[Error]) -> Tuple[int, int, int]:
    """
    Analyzes the list of ChkTeX errors and warnings.

    Returns the number of unique files, errors, and warnings.
    """

    unique_files = set(error.file for error in errors)
    type_counts = Counter(error.type for error in errors)

    number_of_files = len(unique_files)
    number_of_errors = type_counts.get("Error", 0)
    number_of_warnings = type_counts.get("Warning", 0)

    return number_of_files, number_of_errors, number_of_warnings


def main():
    """
    Entry point for the ChkTeX GitHub Action.

    Finds `.tex` files, runs ChkTeX, analyzes results, and writes a Markdown summary.
    """

    github_workspace_path = os.environ.get("GITHUB_WORKSPACE")

    if not github_workspace_path:
        print("No GITHUB_WORKSPACE environment variable set.")

        sys.exit(1)

    tex_files = find_tex_files(github_workspace_path)

    if not tex_files:
        print("::error ::No .tex files found.")

        write_step_summary("## ChkTeX Action Summary\nNo .tex files found.")

        sys.exit(0)

    print("::notice ::Running ChkTeX version 1.7.9")

    errors = run_chktex(github_workspace_path, tex_files)

    number_of_files, number_of_errors, number_of_warnings = analyze_errors(errors)

    step_summary = build_markdown_step_summary(
        errors, number_of_files, number_of_errors, number_of_warnings
    )

    write_step_summary(step_summary)

    if 0 == number_of_files:
        print("::notice ::No errors or warnings found.")

        sys.exit(0)

    print(
        "::error ::Errors: "
        + str(number_of_errors)
        + ", warnings: "
        + str(number_of_warnings)
    )

    sys.exit(1)


if __name__ == "__main__":
    main()
