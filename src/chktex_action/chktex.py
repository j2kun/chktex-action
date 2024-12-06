"""
Provides functionality for running ChkTeX and parsing its output.
"""

import os
import re
import subprocess
from dataclasses import dataclass

from util import Log


@dataclass
class Error:
    """
    Represents a single ChkTeX error or warning.
    """

    level: str
    number: int
    path: str
    line: int
    message: str
    context: list[str]


def parse_chktex_output(stdout: str) -> list[Error]:
    """
    Parses the stdout output from ChkTeX into a list of `Error` objects.

    Extracts details like file, type, line, message, and context.
    """

    pattern = re.compile(
        r"^(Error|Warning)\s+(\d+)\s+in\s+(.*?)\s+line\s+(\d+):\s+(.+)$"
    )

    lines = [line for line in stdout.splitlines() if line.strip()]

    errors = []

    error_index = -1

    for line in lines:
        error_message = pattern.match(line)

        if error_message:
            error = Error(
                error_message.group(1),
                int(error_message.group(2)),
                error_message.group(3),
                int(error_message.group(4)),
                error_message.group(5),
                [],
            )

            errors.append(error)
            error_index = error_index + 1

            continue

        errors[error_index].context.append(line)

    return errors


def find_local_chktexrc(github_workspace_path: str) -> str | None:
    """
    Searches for a local `.chktexrc` configuration file in the workspace.

    Returns the absolute path to the file if found, otherwise `None`.
    """

    os.chdir(github_workspace_path)

    local_chktexrc = os.path.abspath(".chktexrc")

    if os.path.exists(local_chktexrc):
        return local_chktexrc

    return None


def run_chktex(github_workspace_path: str, files: list[str]) -> list[Error]:
    """
    Runs ChkTeX on a list of `.tex` files in the specified workspace.

    Uses either a local `.chktexrc` or the global configuration.
    Returns a list of `Error` objects for any issues found.
    """

    local_chktexrc = find_local_chktexrc(github_workspace_path)

    if local_chktexrc:
        Log.notice("Using local .chktexrc file.")

        def chktex_command(file: str) -> list[str]:
            """Run ChkTeX with the local .chktexrc file."""

            return ["chktex", "-q", "--inputfiles=0", "-l", local_chktexrc, file]

    else:
        Log.notice("Using global chktexrc file.")

        def chktex_command(file: str) -> list[str]:
            """Run ChkTeX with the global chktexrc file."""

            return ["chktex", "-q", "--inputfiles=0", file]

    total_errors = []

    for file in files:
        Log.debug("Linting file: " + file)

        completed_process = subprocess.run(
            chktex_command(file),
            cwd=github_workspace_path,
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
