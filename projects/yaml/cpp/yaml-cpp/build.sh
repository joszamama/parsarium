#!/bin/sh
set -eu
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -DYAML_CPP_STATIC_DEFINE'
sources=$(ls /work/source/src/*.cpp /work/source/src/contrib/*.cpp)
includes='-I/work/source/include -I/work/source/src'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $includes \
  $sources /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $includes \
  $sources /work/harness.cpp -o /work/fuzzer
