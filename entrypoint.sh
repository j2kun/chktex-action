#!/bin/bash
set -e
set -o pipefail

# chktex doesn't have the proper exit status when it reports linter issues,
# instead it always exits with status 0. Here we check if the output is empty
# and if not, print the linter errors and exit 1.

# -q suppresses version information
OUTPUT=$(for line in $(git ls-files --full-name | grep "\.tex$"); do; chktex -q "$GITHUB_WORKSPACE/$line"; done)

if [[ $OUTPUT ]]; then
    echo "$OUTPUT"
    exit 1
fi
