#!/bin/sh
set -eu
mkdir -p /work/cov /work/fuzz
common='-O1 -g -fno-omit-frame-pointer -DNO_PNG -DNO_JPEG -I/work/source/src'
for source in /work/source/src/*.c; do
  name=$(basename "$source" .c)
  clang $common -fprofile-instr-generate -fcoverage-mapping -c "$source" -o "/work/cov/$name.o"
  clang $common -fsanitize=fuzzer-no-link,address,undefined -c "$source" -o "/work/fuzz/$name.o"
done
ar rcs /work/libimago-cov.a /work/cov/*.o
ar rcs /work/libimago-fuzz.a /work/fuzz/*.o
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c /work/libimago-cov.a -ldl -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c /work/libimago-fuzz.a -ldl -o /work/fuzzer
