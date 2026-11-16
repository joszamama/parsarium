#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer -I/work/source'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c -o /work/fuzzer
