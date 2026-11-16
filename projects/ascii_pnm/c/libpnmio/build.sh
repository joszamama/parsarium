#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer -I/work/source/src'
clang $common -fprofile-instr-generate -fcoverage-mapping -c /work/source/src/pnmio.c -o /work/parser-cov.o
clang $common -fsanitize=fuzzer-no-link,address,undefined -c /work/source/src/pnmio.c -o /work/parser-fuzz.o
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c /work/parser-cov.o -lm -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c /work/parser-fuzz.o -lm -o /work/fuzzer
