#!/bin/sh
set -eu
includes='-I/work/source/gil/include -I/work/source/boost'
clang++ -std=c++17 -O1 -g -fprofile-instr-generate -fcoverage-mapping $includes /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ -std=c++17 -O1 -g -fsanitize=fuzzer,address,undefined $includes /work/harness.cpp -o /work/fuzzer
