#!/bin/sh
set -eu

common='-std=c++17 -O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/lodepng-src /work/harness.cpp /work/replay.cpp \
  /work/lodepng-src/lodepng.cpp -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined \
  -I/work/lodepng-src /work/harness.cpp /work/lodepng-src/lodepng.cpp \
  -o /work/fuzzer
