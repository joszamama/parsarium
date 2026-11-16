#!/bin/sh
set -eu
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -I/work/install/include -L/work/install/lib -lsfml-audio -lsfml-system -Wl,-rpath,/work/install/lib -Wl,-export-dynamic'
clang++ -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp $common -o /work/replay
clang++ -fsanitize=fuzzer,address,undefined /work/harness.cpp $common -o /work/fuzzer
