"""
Contains various helper functions, classes, and methods.
"""

import os
from collections import Counter
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chktex import Error


@dataclass
class Analysis:
    """
    Represents an analysis result.
    """

    number_of_files: int
    number_of_errors: int
    number_of_warnings: int


class Log:
    """
    Contains static methods for logging to the GitHub workflow console.
    """

    prefix = " ::ChkTeX Action: "

    @staticmethod
    def error(message: str) -> None:
        """
        Logs an error.
        """

        print("::error" + Log.prefix + message)

    @staticmethod
    def notice(message: str) -> None:
        """
        Logs a notice.
        """

        print("::notice" + Log.prefix + message)

    @staticmethod
    def debug(message: str) -> None:
        """
        Logs a debug message if debugging is enabled.
        """

        if "1" == os.environ.get("RUNNER_DEBUG", ""):
            print("::debug" + Log.prefix + message)


def get_analysis_string(analysis: Analysis) -> str:
    """
    Creates a string representation of the analysis result.
    """

    return (
        f"Total files: {analysis.number_of_files}, total errors: "
        f"{analysis.number_of_errors}, total warnings: {analysis.number_of_warnings}"
    )


def is_push() -> bool:
    """
    Checks if the workflow trigger was a push.
    """

    return "push" == os.environ.get("GITHUB_EVENT_NAME")


def is_pull_request() -> bool:
    """
    Checks if the workflow trigger was a pull request.
    """

    return "pull_request" == os.environ.get("GITHUB_EVENT_NAME")


def is_lint_all_enabled() -> bool:
    """
    Checks if the `lint-all` input was set to `true`.
    """

    return "true" == os.environ.get("INPUT_LINT-ALL")


def analyze_errors(errors: list["Error"]) -> Analysis:
    """
    Analyzes the list of ChkTeX errors and warnings.

    Returns the number of unique files, errors, and warnings.
    """

    unique_files = set(error.path for error in errors)

    level_counts = Counter(error.level for error in errors)

    number_of_errors = level_counts.get("Error", 0)

    number_of_warnings = level_counts.get("Warning", 0)

    return Analysis(len(unique_files), number_of_errors, number_of_warnings)
