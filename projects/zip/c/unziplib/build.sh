#!/bin/sh
set -eu
mkdir -p /work/cov /work/fuzz
common='-O1 -g -fno-omit-frame-pointer -D__LINUX__ -I/work/source/src'
for source in unzip adler32 crc32 infback inffast inflate inftrees zutil; do
  clang $common -fprofile-instr-generate -fcoverage-mapping -c "/work/source/src/$source.c" -o "/work/cov/$source.o"
  clang $common -fsanitize=fuzzer-no-link,address,undefined -c "/work/source/src/$source.c" -o "/work/fuzz/$source.o"
done
ar rcs /work/unzip-cov.a /work/cov/*.o
ar rcs /work/unzip-fuzz.a /work/fuzz/*.o
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c /work/unzip-cov.a -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c /work/unzip-fuzz.a -o /work/fuzzer
