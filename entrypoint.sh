#!/bin/bash
set -euf -o pipefail

FILES=$(git ls-files --full-name | grep "\.tex$" || true)

if [ -z "$FILES" ]
then
      echo "Found no files to lint; ran 'git ls-files --full-name | grep \"\.tex$\"'"
      exit 0
fi


# chktex doesn't have the proper exit status when it reports linter issues,
# instead it always exits with status 0. So we run chktex on each file in the repo,
# combine the output into a single string, and fail if that string is nonempty
OUTPUT=""

echo "$FILES" | while read line
do
    CHKTEX_ARG="$GITHUB_WORKSPACE/$line"
    echo "Linting $CHKTEX_ARG"

    # -q suppresses version information so that empty output means it lints
    SINGLE_CMD_OUTPUT=$(chktex -q "$CHKTEX_ARG")

    echo "$SINGLE_CMD_OUTPUT"
    OUTPUT+="$SINGLE_CMD_OUTPUT"
done

if [[ $OUTPUT ]]; then
    exit 1
fi
