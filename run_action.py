import os
import sys
from github import Github

SKIP_DIRS = set(['venv', '.git', '__pycache__'])


GITHUB_WORKSPACE = os.environ.get('GITHUB_WORKSPACE')
if not GITHUB_WORKSPACE:
    print("No GITHUB_WORKSPACE environment variable set.")
    sys.exit(1)

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("No GITHUB_TOKEN environment variable set.")
    sys.exit(1)

os.chdir(GITHUB_WORKSPACE)
g = Github(GITHUB_TOKEN)

all_files_in_tree = []
for root, dirs, files in os.walk(".", topdown=True):
    for d in SKIP_DIRS:
        if d in dirs:
            dirs.remove(d)

    for filename in files:
        all_files_in_tree.append(os.path.join(root, filename))

files_to_process = [filename for filename in all_files_in_tree if filename.endswith(".tex")]

if not files_to_process:
    print("Found no .tex files to process")
    print("Complete tree found:")
    for filename in all_files_in_tree:
        print(filename)
    sys.exit(1)

for filename in files_to_process:
    print("Linting %s" % filename)
