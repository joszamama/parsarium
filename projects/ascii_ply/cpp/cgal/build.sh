#!/bin/sh
set -eu

common='-std=c++17 -O1 -g -fno-omit-frame-pointer -I/work/source/include'
clang++ $common -fprofile-instr-generate -fcoverage-mapping \
  /work/harness.cpp /work/replay.cpp -lgmp -lmpfr -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined \
  /work/harness.cpp /work/fuzz.cpp -lgmp -lmpfr -o /work/fuzzer
