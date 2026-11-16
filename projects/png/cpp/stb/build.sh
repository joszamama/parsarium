#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer'
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/stb /work/harness.cpp /work/replay.cpp -lm -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined \
  -I/work/stb /work/harness.cpp -lm -o /work/fuzzer
