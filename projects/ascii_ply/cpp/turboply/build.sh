#!/bin/sh
set -eu
common='-std=c++20 -O1 -g -fno-omit-frame-pointer -I/work/source -include algorithm -include format -include charconv -include cstring'
clang++ $common -fprofile-instr-generate -fcoverage-mapping \
    /work/source/plyfile.cpp /work/source/plystream.cpp \
    /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined \
    /work/source/plyfile.cpp /work/source/plystream.cpp \
    /work/harness.cpp -o /work/fuzzer
