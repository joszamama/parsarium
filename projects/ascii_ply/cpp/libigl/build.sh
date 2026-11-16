#!/bin/sh
set -eu

common='-std=c++17 -O1 -g -fno-omit-frame-pointer -I/work/source/include -I/usr/include/eigen3'
clang++ $common -fprofile-instr-generate -fcoverage-mapping \
  /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined \
  /work/harness.cpp /work/fuzz.cpp -o /work/fuzzer
