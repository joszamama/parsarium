#!/usr/bin/env bash
set -euo pipefail

args=()
for arg in "$@"; do
  if [[ "$arg" == "--Output=XML" ]]; then
    args+=("--Output=OLDXML")
  else
    args+=("$arg")
  fi
done
exec mediainfo "${args[@]}"
