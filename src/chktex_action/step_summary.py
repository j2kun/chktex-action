"""
Handles building and writing Markdown summaries of ChkTeX results.

Generates formatted Markdown for errors and writes it to the GitHub Actions step
summary.
"""

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chktex import Error

ERROR_MARKDOWN = """### Path: {0}

- **Type**: {1} {2}
- **Line**: {3}
- **Message**: {4}
- **Context**:

{5}
"""


def build_markdown_step_summary(errors: list["Error"], analysis_string: str) -> str:
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
                error.path,
                error.level,
                error.number,
                error.line,
                error.message,
                context,
            )
        )

    return f"{analysis_string}\n" + "\n".join(formatted_errors)


def write_step_summary(step_summary: str) -> None:
    """
    Writes the provided Markdown summary to the `GITHUB_STEP_SUMMARY` file.
    """

    step_summary_file: str = os.environ.get("GITHUB_STEP_SUMMARY", "")

    with open(step_summary_file, "a", encoding="utf-8") as github_step_summary:
        github_step_summary.write("## ChkTeX Action Summary\n" + step_summary)
