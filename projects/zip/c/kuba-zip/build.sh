#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/source/src \
  -c /work/source/src/zip.c -o /work/zip-cov.o
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/source/src \
  /work/harness.c /work/replay.c /work/zip-cov.o -lm -o /work/replay
clang $common -fsanitize=fuzzer-no-link,address,undefined -I/work/source/src \
  -c /work/source/src/zip.c -o /work/zip-fuzz.o
clang $common -fsanitize=fuzzer,address,undefined -I/work/source/src \
  /work/harness.c /work/zip-fuzz.o -lm -o /work/fuzzer
