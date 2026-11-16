#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer -I/work/source/Sources'
for unit in llhttp api http; do
  clang $common -fprofile-instr-generate -fcoverage-mapping -c "/work/source/Sources/$unit.c" -o "/work/$unit-cov.o"
  clang $common -fsanitize=fuzzer-no-link,address,undefined -c "/work/source/Sources/$unit.c" -o "/work/$unit-fuzz.o"
done
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c /work/*-cov.o -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c /work/*-fuzz.o -o /work/fuzzer
