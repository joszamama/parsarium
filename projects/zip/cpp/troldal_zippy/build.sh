#!/bin/sh
set -eu
if command -v afl-fuzz >/dev/null 2>&1; then
    common='-std=c++17 -O0 -g -fno-omit-frame-pointer -I/work/source/library'
    fuzz_flags='-fsanitize=fuzzer'
else
    common='-std=c++17 -O1 -g -fno-omit-frame-pointer -I/work/source/library'
    fuzz_flags='-fsanitize=fuzzer,address,undefined'
fi
clang++ $common -fprofile-instr-generate -fcoverage-mapping \
    /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ $common $fuzz_flags \
    /work/harness.cpp -o /work/fuzzer
