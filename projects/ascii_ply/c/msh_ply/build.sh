#!/bin/sh
set -eu
common='-std=c11 -O1 -g -fno-omit-frame-pointer -D_GNU_SOURCE -I/work/source'
clang $common -fprofile-instr-generate -fcoverage-mapping \
    /work/harness.c /work/replay.c -o /work/replay
fuzz_extra=''
if command -v afl-fuzz >/dev/null 2>&1; then
    fuzz_extra='-fno-sanitize=alignment'
fi
clang $common -fsanitize=fuzzer,address,undefined $fuzz_extra \
    /work/harness.c -o /work/fuzzer
