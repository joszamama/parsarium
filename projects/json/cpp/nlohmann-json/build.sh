#!/bin/sh
set -eu
common='-std=c++17 -O1 -g -fno-omit-frame-pointer'
includes='-I/work/source/include'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $includes \
  /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $includes \
  /work/harness.cpp -o /work/fuzzer
