"""
Provides functionality for running ChkTeX and parsing its output.
"""

import re
from subprocess import run
from dataclasses import dataclass
from typing import List, LiteralString
from os import path, chdir


@dataclass
class Error:
    """
    Represents a single ChkTeX error or warning.
    """

    file: str
    type: str
    number: int
    line: int
    message: str
    context: List[str]


def parse_chktex_output(stdout: str) -> List[Error]:
    """
    Parses the stdout output from ChkTeX into a list of `Error` objects.

    Extracts details like file, type, line, message, and context.
    """

    pattern = re.compile(
        r"^(Error|Warning)\s+(\d+)\s+in\s+(.*?)\s+line\s+(\d+):\s+(.+)$"
    )

    lines = [line for line in stdout.splitlines() if line.strip()]
    errors = []
    index = -1

    for line in lines:
        error_message = pattern.match(line)

        if error_message:
            error = Error(
                type=error_message.group(1),
                number=int(error_message.group(2)),
                file=error_message.group(3),
                line=int(error_message.group(4)),
                message=error_message.group(5),
                context=[],
            )

            errors.append(error)

            index = index + 1

            continue

        errors[index].context.append(line)

    return errors


def find_local_chktexrc(github_workspace_path: str) -> str | None:
    """
    Searches for a local `.chktexrc` configuration file in the workspace.

    Returns the absolute path to the file if found, otherwise `None`.
    """

    chdir(github_workspace_path)
    local_chktexrc = path.abspath(".chktexrc")

    if path.exists(local_chktexrc):
        return local_chktexrc

    return None


def run_chktex(
    github_workspace_path: str, files: list[LiteralString | str | bytes]
) -> List[Error]:
    """
    Runs ChkTeX on a list of `.tex` files in the specified workspace.

    Uses either a local `.chktexrc` or the global configuration.
    Returns a list of `Error` objects for any issues found.
    """

    local_chktexrc = find_local_chktexrc(github_workspace_path)

    if local_chktexrc:
        print("::notice ::Using local .chktexrc file.")

        def chktex_command(file):
            """Run ChkTeX with the local .chktexrc file."""

            return ["chktex", "-q", "--inputfiles=0", "-l", local_chktexrc, file]

    else:
        print("::notice ::Using global chktexrc file.")

        def chktex_command(file):
            """Run ChkTeX with the global chktexrc file."""

            return ["chktex", "-q", "--inputfiles=0", file]

    total_errors = []

    for file in files:
        directory = path.dirname(file)
        relative_file = path.basename(file)

        completed_process = run(
            chktex_command(relative_file),
            cwd=directory,
            capture_output=True,
            text=True,
            check=False,
        )

        stdout = completed_process.stdout
        # Mark as unused, might be used later
        _stderr = completed_process.stderr  # noqa: F841

        errors = parse_chktex_output(stdout)

        total_errors.extend(errors)

    return total_errors
