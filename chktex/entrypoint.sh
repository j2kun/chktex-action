#!/bin/bash
set -e
set -o pipefail

# TODO: build a map from file to errors, only process files that were
# changed in the context PR
if [[ -z "$TEX_MAIN" ]]; then
  echo "Set the TEX_MAIN env variable to choose which file to lint."
  exit 1
fi

# use path.join in python
chktex "$GITHUB_WORKSPACE/$TEX_MAIN"
