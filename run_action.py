import os
import subprocess
import sys

SKIP_DIRS = set(["venv", ".git", "__pycache__"])


GITHUB_WORKSPACE = os.environ.get("GITHUB_WORKSPACE")
if not GITHUB_WORKSPACE:
    print("No GITHUB_WORKSPACE environment variable set.")
    sys.exit(1)


def main():
    os.chdir(GITHUB_WORKSPACE)

    all_files_in_tree = []
    for root, dirs, files in os.walk(".", topdown=True):
        for skip_dir in SKIP_DIRS:
            if skip_dir in dirs:
                dirs.remove(skip_dir)

        for filename in files:
            all_files_in_tree.append(os.path.join(root, filename))

    files_to_process = [
        filename for filename in all_files_in_tree if filename.endswith(".tex")
    ]

    if not files_to_process:
        print("Found no .tex files to process")
        print("Complete tree found:")
        for filename in all_files_in_tree:
            print(filename)
        sys.exit(0)

    num_linter_errors = 0

    for filename in files_to_process:
        print("Linting %s\n" % filename)
        completed_process = subprocess.run(
            ["chktex", "-q", filename], capture_output=True, text=True, check=False
        )
        stdout = completed_process.stdout

        if stdout:
            num_linter_errors += 1
            print(stdout)

    if num_linter_errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
