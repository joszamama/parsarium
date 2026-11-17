#!/bin/sh
set -eu

# AFL++'s libFuzzer-compatible driver waits for input with no arguments.
# Discover the compiled map size with one fixed, valid P3 control instead.
report=$(mktemp)
edges=$(mktemp)
trap 'rm -f "$report" "$edges"' EXIT
if ! env -u AFL_DUMP_MAP_SIZE afl-showmap -m none -t 10000 -o "$edges" -- \
        /work/replay /work/map-control.ppm >"$report" 2>&1; then
    cat "$report" >&2
    exit 1
fi
size=$(sed -n 's/.*Acquired new map size for target: \([0-9][0-9]*\) bytes.*/\1/p' "$report" | head -n 1)
test -n "$size"
test -s "$edges"
printf '%s\n' "$size"
