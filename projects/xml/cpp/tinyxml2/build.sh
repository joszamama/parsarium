#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping -I/work/source \
  /work/source/tinyxml2.cpp /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -I/work/source \
  /work/source/tinyxml2.cpp /work/harness.cpp -o /work/fuzzer
