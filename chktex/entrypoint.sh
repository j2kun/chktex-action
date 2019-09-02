#!/bin/sh -l

set -eu

if [[ -z "$TEX_MAIN" ]]; then
  TEX_MAIN="--version"
fi

chktex $TEX_MAIN
