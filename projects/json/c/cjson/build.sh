#!/bin/sh
set -eu
common='-std=c11 -O1 -g -fno-omit-frame-pointer -I/work/cjson-src'
clang $common -fprofile-instr-generate -fcoverage-mapping \
    /work/harness.c /work/cjson-src/cJSON.c -lm -o /work/replay
clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined \
    /work/harness.c /work/cjson-src/cJSON.c -lm -o /work/fuzzer
