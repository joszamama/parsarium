#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/stb /work/harness.c /work/replay.c -lm -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined \
  -I/work/stb /work/harness.c -lm -o /work/fuzzer
