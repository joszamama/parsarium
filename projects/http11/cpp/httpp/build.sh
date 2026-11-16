#!/bin/sh
set -eu
src=/work/httpp-2.0.0
common='-O1 -g -fno-omit-frame-pointer'
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
  /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -I"$src" \
  /work/harness.cpp -o /work/fuzzer
