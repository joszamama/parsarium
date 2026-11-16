#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer -I/work/install/include -L/work/install/lib -lalut -lopenal -Wl,-rpath,/work/install/lib -Wl,-export-dynamic'
clang++ -std=c++17 -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp $common -o /work/replay
clang++ -std=c++17 -fsanitize=fuzzer,address,undefined /work/harness.cpp $common -o /work/fuzzer
