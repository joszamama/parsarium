#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer -std=c++17'
clang++ $common -fprofile-instr-generate -fcoverage-mapping -I/work/source/include /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined -I/work/source/include /work/harness.cpp -o /work/fuzzer
