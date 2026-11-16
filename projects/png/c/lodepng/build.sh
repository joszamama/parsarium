#!/bin/sh
set -eu
common='-std=c11 -O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/lodepng-src /work/harness.c /work/replay.c \
  /work/lodepng-src/lodepng.c -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined \
  -I/work/lodepng-src /work/harness.c /work/lodepng-src/lodepng.c \
  -o /work/fuzzer
