#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer -I/work/source'
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping \
  /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined \
  /work/harness.cpp -o /work/fuzzer
