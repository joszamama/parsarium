#!/bin/sh
# Usage: probe.sh CONTROL|--baseline  (baseline runs node without calling JSON.parse)
set -eu
if [ "$1" = --baseline ]; then set -- /usr/local/bin/node -e 0; else set -- /usr/local/bin/node /work/adapter.mjs "$1"; fi
gdb -q -batch -nx -x /work/probe.py --args "$@" 2>/dev/null | grep -E '^(SYMBOLS|HIT) '
