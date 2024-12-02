"""
Handles building and writing Markdown summaries of ChkTeX results.

Generates formatted Markdown for errors and writes it to the GitHub Actions step
summary.
"""

from os import environ
from typing import List
from chktex import Error

HEADER_MARKDOWN = """## ChkTeX Action Summary

Total files: {0}, total errors: {1}, total warnings: {2}

"""

ERROR_MARKDOWN = """### File: {0}

- **Type**: {1} {2}
- **Line**: {3}
- **Message**: {4}
- **Context**:

{5}
"""


def build_markdown_step_summary(
    errors: List[Error],
    number_of_files: int,
    number_of_errors: int,
    number_of_warnings: int,
) -> str:
    """
    Builds a Markdown summary from the list of ChkTeX errors.

    Includes the total number of files, errors, and warnings, along with details for
    each error or warning.
    """

    formatted_errors = []

    for error in errors:
        error.message = error.message.replace("`", r"\`")

        if not error.context:
            context = """```text\nNo context\n```"""
        else:
            context = "\n".join(["```tex"] + error.context + ["```"])

        formatted_errors.append(
            ERROR_MARKDOWN.format(
                error.file,
                error.type,
                error.number,
                error.line,
                error.message,
                context,
            )
        )

    return HEADER_MARKDOWN.format(
        number_of_files, number_of_errors, number_of_warnings
    ) + "\n".join(formatted_errors)


def write_step_summary(step_summary: str) -> None:
    """
    Writes the provided Markdown summary to the `GITHUB_STEP_SUMMARY` file.
    """

    with open(
        environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8"
    ) as github_step_summary:
        github_step_summary.write(step_summary)
