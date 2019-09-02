#!/bin/bash
set -e
set -o pipefail

# TODO: build a map from file to errors, only process files that were
# changed in the context PR
if [[ -z "$TEX_MAIN" ]]; then
  echo "Set the TEX_MAIN env variable to choose which file to lint."
  exit 1
fi

# chktex doesn't have the proper exit status when it reports linter issues,
# instead it always exits with status 0. Here we check if the output is empty
# and if not, print the linter errors and exit 1.

# -q suppresses version information
OUTPUT=$(for line in $(git ls-files --full-name | grep "\.tex$"); do; chktex -q "$GITHUB_WORKSPACE/$TEX_MAIN"; done)

if [[ $OUTPUT ]]; then
    echo "$OUTPUT"
    exit 1
fi
