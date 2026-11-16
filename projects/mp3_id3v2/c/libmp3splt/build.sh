#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer -I/work/install/include/libmp3splt -L/work/install/lib -lmp3splt -Wl,-rpath,/work/install/lib -Wl,-export-dynamic'
clang -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c $common -o /work/replay
clang -fsanitize=fuzzer,address,undefined /work/harness.c $common -o /work/fuzzer
