#!/bin/sh
set -eu
src=/work/boost_1_92_0
common='-std=c++17 -O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
  /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined -I"$src" \
  /work/harness.cpp -o /work/fuzzer
