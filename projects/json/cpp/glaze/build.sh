#!/bin/sh
set -eu
common='-std=c++23 -O1 -g -fno-omit-frame-pointer -I/work/source/include'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp -o /work/replay
clang++ $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.cpp -o /work/fuzzer
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.cpp -o /work/parser-probe
clang++ $common -fsanitize=address,undefined /work/parser-probe.cpp -o /work/parser-probe-afl
