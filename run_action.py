"""Find all *.tex files and run ChkTeX on them"""

import os
import subprocess
import sys
from dataclasses import dataclass


@dataclass
class Result:
    """Represents the details of a .tex file that ChkTeX marked with errors."""

    filename: str
    success: bool
    stdout: str
    stderr: str


def find_files_to_process(github_workspace_path=None):
    """
    Returns a list of absolute filepaths of files with filenames ending in .tex in the
    GitHub workspace directory.
    Those are the files that should be linted.
    """

    github_workspace_path = github_workspace_path or os.environ.get("GITHUB_WORKSPACE")

    all_files_in_tree = []
    skip_dirs = {"venv", ".git", "__pycache__"}

    for root, dirs, files in os.walk(github_workspace_path, topdown=True):
        for skip_dir in skip_dirs:
            if skip_dir in dirs:
                dirs.remove(skip_dir)

        for file in files:
            all_files_in_tree.append(os.path.join(root, file))

    return [file for file in all_files_in_tree if file.endswith(".tex")]


def find_chktexrc(github_workspace_path=None):
    """
    Return the absolute path of the .chktexrc file in the workspace if one exists.
    Otherwise, return None.
    """

    os.chdir(github_workspace_path)
    locale_chktexrc = os.path.abspath(".chktexrc")

    if os.path.exists(locale_chktexrc):
        return locale_chktexrc

    return None


def failing_files(files=None, command=None):
    """
    Run the given chktex command on the list of files, and return a list of detail
    objects for the runs that failed.
    """

    error_details = []

    for file in files:
        directory = os.path.dirname(file)
        relative_file = os.path.basename(file)

        # run process inside the file's folder
        completed_process = subprocess.run(
            command(relative_file),
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
        )

        stdout = completed_process.stdout
        stderr = completed_process.stderr

        result = Result(
            filename=file,
            success=len(stdout) + len(stderr) == 0,
            stdout=stdout,
            stderr=stderr,
        )

        if not result.success:
            error_details.append(result)

    return error_details


if __name__ == "__main__":
    GITHUB_WORKSPACE = os.environ.get("GITHUB_WORKSPACE")

    if not GITHUB_WORKSPACE:
        print("No GITHUB_WORKSPACE environment variable set.")

        sys.exit(1)

    files_to_process = find_files_to_process(github_workspace_path=GITHUB_WORKSPACE)

    if not files_to_process:
        print("Found no .tex files to process")

        sys.exit(0)

    chktexrc = find_chktexrc(github_workspace_path=GITHUB_WORKSPACE)

    if chktexrc:
        print("Using local .chktexrc")

        def chktex_command(file):
            """Run ChkTeX with the local .chktexrc file."""

            return ["chktex", "-q", "--inputfiles=0", "-l", chktexrc, file]

    else:

        def chktex_command(file):
            """Run ChkTeX with the global .chktexrc file."""

            return ["chktex", "-q", "--inputfiles=0", file]

    failing_file_info = failing_files(files_to_process, chktex_command)

    if not failing_file_info:
        print("No errors found")

        sys.exit(0)

    for failing_file_details in failing_file_info:
        print(
            "=" * 50,
            "Linting " + failing_file_details.filename,
            "-" * 50,
            failing_file_details.stdout,
            "=" * 50,
            sep="\n",
        )

    NUMBER_OF_FAILED_FILES = str(len(failing_file_info))

    print("Errors found in " + NUMBER_OF_FAILED_FILES + " file(s)")

    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as github_output:
        github_output.write("number-of-failed-files=" + NUMBER_OF_FAILED_FILES)

    sys.exit(1)
