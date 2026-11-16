#!/bin/sh
set -eu
common='-std=c11 -O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/libspng-src/spng /work/harness.c /work/replay.c \
  /work/libspng-src/spng/spng.c -lz -lm -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined \
  -I/work/libspng-src/spng /work/harness.c /work/libspng-src/spng/spng.c \
  -lz -lm -o /work/fuzzer
