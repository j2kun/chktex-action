"""Find all *tex files and run chktex on them"""

import os
import subprocess
import sys

SKIP_DIRS = set(["venv", ".git", "__pycache__"])


GITHUB_WORKSPACE = os.environ.get("GITHUB_WORKSPACE")
if not GITHUB_WORKSPACE:
    print("No GITHUB_WORKSPACE environment variable set.")
    sys.exit(1)

os.chdir(GITHUB_WORKSPACE)


CHKTEXRC = os.path.abspath(".chktexrc")
if os.path.exists(CHKTEXRC):
    print("found local chktexrc")
    CHKTEX_COMMAND = lambda file: ["chktex", "-q", "-l", CHKTEXRC, file]
else:
    CHKTEX_COMMAND = lambda file: ["chktex", "-q", file]


def main():
    """main function"""

    all_files_in_tree = []
    for root, dirs, files in os.walk(".", topdown=True):
        for skip_dir in SKIP_DIRS:
            if skip_dir in dirs:
                dirs.remove(skip_dir)

        for file in files:
            all_files_in_tree.append(os.path.join(root, file))

    files_to_process = [file for file in all_files_in_tree if file.endswith(".tex")]

    if not files_to_process:
        print("Found no .tex files to process")
        print("Complete tree found:")
        for file in all_files_in_tree:
            print(file)
        sys.exit(0)

    files_with_errors = 0

    for file in files_to_process:
        print(f"Linting {file}")

        directory = os.path.dirname(file)
        relative_file = os.path.basename(file)

        # run process inside the file's folder
        completed_process = subprocess.run(
            CHKTEX_COMMAND(relative_file),
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
        )
        stdout = completed_process.stdout
        stderr = completed_process.stderr

        if stdout:
            files_with_errors += 1
            print(
                "----------------------------------------",
                stdout,
                "----------------------------------------",
                sep="\n",
            )

        if stderr:
            print("chktex run into errors:", stderr, sep="\n")

    print(f"found {files_with_errors} files with errors")
    sys.exit(files_with_errors)


if __name__ == "__main__":
    main()
