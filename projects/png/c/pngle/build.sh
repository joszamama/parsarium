#!/bin/sh
set -eu
common='-std=c11 -O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/pngle-src/src /work/harness.c /work/replay.c \
  /work/pngle-src/src/pngle.c /work/pngle-src/src/miniz.c -lm -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined \
  -I/work/pngle-src/src /work/harness.c \
  /work/pngle-src/src/pngle.c /work/pngle-src/src/miniz.c -lm -o /work/fuzzer
