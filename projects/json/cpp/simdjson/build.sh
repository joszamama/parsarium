#!/bin/sh
set -eu
common='-std=c++20 -O1 -g -fno-omit-frame-pointer -I/work/source/singleheader'
clang++ $common -fprofile-instr-generate -fcoverage-mapping \
    /work/harness.cpp /work/source/singleheader/simdjson.cpp -o /work/replay
clang++ $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined \
    /work/harness.cpp /work/source/singleheader/simdjson.cpp -o /work/fuzzer
