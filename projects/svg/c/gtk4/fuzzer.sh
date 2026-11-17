#!/bin/sh
if [ "${AFL_DUMP_MAP_SIZE:-}" = 1 ]; then
    exec /work/replay-bin
fi
exec /work/with-display.sh /work/fuzzer-bin "$@"
