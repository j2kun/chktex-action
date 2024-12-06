"""
Main module for finding `.tex` files and running ChkTeX on them.

Includes logic to parse files, run ChkTeX, analyze errors, and write a Markdown summary
for GitHub Actions.
"""

import glob
import importlib
import os
import sys

from chktex import run_chktex
from github import Auth, Github
from pull_request import get_pull_request_number, process_pull_request
from step_summary import build_markdown_step_summary, write_step_summary
from util import (
    Log,
    analyze_errors,
    get_analysis_string,
    is_lint_all_enabled,
    is_pull_request,
    is_push,
)

# Only enable debugging when not running on GitHub Actions
if not os.environ.get("GITHUB_ACTIONS"):
    try:
        pydevd_pycharm = importlib.import_module("pydevd_pycharm")

        pydevd_pycharm.settrace(
            "host.docker.internal",
            port=4567,
            stdoutToServer=True,
            stderrToServer=True,
            suspend=False,
        )
    except ImportError:
        print("pydevd_pycharm is not installed. Debugging is disabled.")


def main() -> None:
    """
    Entry point for the ChkTeX GitHub Action.

    Finds `.tex` files, runs ChkTeX, analyzes results, and writes a Markdown summary.
    """

    if not (is_push() or is_pull_request()):
        Log.error("Only pull_request or push triggers are supported.")

        sys.exit(1)

    github_workspace_path = os.environ.get("GITHUB_WORKSPACE", "")

    token = Auth.Token(os.environ.get("INPUT_GITHUB-TOKEN", ""))

    github = Github(auth=token)

    repository = github.get_repo(os.environ.get("GITHUB_REPOSITORY", ""))

    pull_request = None

    if is_pull_request() and not is_lint_all_enabled():
        pull_request = repository.get_pull(get_pull_request_number())

        files = [
            file.filename
            for file in pull_request.get_files()
            if file.filename.endswith(".tex")
        ]
    elif is_push() and not is_lint_all_enabled():
        latest_commit = repository.get_branch(
            os.environ.get("GITHUB_REF_NAME", "")
        ).commit

        files = [
            file.filename
            for file in latest_commit.files
            if file.filename.endswith(".tex")
        ]
    else:
        files = glob.glob("**/*.tex", root_dir=github_workspace_path, recursive=True)

    if not files:
        Log.error("No .tex files found.")

        write_step_summary("No .tex files found.")

        sys.exit(0)

    Log.notice("Running ChkTeX version 1.7.9")

    errors = run_chktex(github_workspace_path, files)

    analysis = analyze_errors(errors)

    analysis_string = get_analysis_string(analysis)

    if is_pull_request() and pull_request and not is_lint_all_enabled():
        latest_commit = repository.get_branch(
            os.environ.get("GITHUB_HEAD_REF", "")
        ).commit

        check_run = latest_commit.get_check_runs()[0]

        process_pull_request(pull_request, check_run, errors, analysis_string)

    step_summary = build_markdown_step_summary(errors, analysis_string)

    write_step_summary(step_summary)

    if 0 == analysis.number_of_files:
        Log.notice("No errors or warnings found.")

        sys.exit(0)

    Log.error(analysis_string)

    sys.exit(1)


if __name__ == "__main__":
    main()
