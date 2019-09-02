#!/bin/bash
set -o pipefail

FILES=$(git ls-files --full-name | grep "\.tex$")

if [ -z "$FILES" ]
then
      echo "Found no files to lint; ran 'git ls-files --full-name | grep \"\.tex$\"'"
      exit 0
fi


# chktex doesn't have the proper exit status when it reports linter issues,
# instead it always exits with status 0. So we run chktex on each file in the repo,
# combine the output into a single string, and fail if that string is nonempty
OUTPUT=""

for line in
do
    # -q suppresses version information
    OUTPUT+=$(chktex -q "$GITHUB_WORKSPACE/$line")
done

if [[ $OUTPUT ]]; then
    echo "$OUTPUT"
    exit 1
fi
