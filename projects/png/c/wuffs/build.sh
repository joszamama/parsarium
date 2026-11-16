#!/bin/sh
set -eu
common='-std=c11 -O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/wuffs-src/release/c /work/harness.c /work/replay.c -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined \
  -I/work/wuffs-src/release/c /work/harness.c -o /work/fuzzer
