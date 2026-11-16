#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer -I/work/source/include -L/work/source/build/shared-release -lmupdf -Wl,-rpath,/work/lib -Wl,-export-dynamic'
clang++ -std=c++17 -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp $common -o /work/replay
clang++ -std=c++17 -fsanitize=fuzzer,address,undefined /work/harness.cpp $common -o /work/fuzzer
