#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer -I/work/source'
clang++ $common -fprofile-instr-generate -fcoverage-mapping \
  /work/harness.cpp /work/replay.cpp -lm -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined \
  /work/harness.cpp -lm -o /work/fuzzer
