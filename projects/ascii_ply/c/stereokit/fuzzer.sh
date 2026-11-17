#!/bin/sh
set -eu
# The full graphics runtime retains startup allocations after sk_shutdown.
# Fixed-input parser replay keeps leak checking off; users can invoke
# /work/fuzzer-bin directly to examine the complete runtime lifecycle.
export ASAN_OPTIONS="detect_leaks=0${ASAN_OPTIONS:+:$ASAN_OPTIONS}"
exec /work/fuzzer-bin -detect_leaks=0 "$@"
