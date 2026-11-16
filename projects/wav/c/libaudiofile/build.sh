#!/bin/sh
set -eu
cd /work/source
CC=clang CXX=clang++ CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --disable-shared --enable-static
make -C libaudiofile -j 4
common='-O1 -g -fno-omit-frame-pointer -I/work/source -I/work/source/libaudiofile'
clang $common -fprofile-instr-generate -fcoverage-mapping -c /work/harness.c -o /work/harness-cov.o
clang $common -fsanitize=fuzzer-no-link,address,undefined -c /work/harness.c -o /work/harness-fuzz.o
clang $common -fprofile-instr-generate -fcoverage-mapping -c /work/replay.c -o /work/replay.o
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness-cov.o /work/replay.o /work/source/libaudiofile/.libs/libaudiofile.a -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness-fuzz.o /work/source/libaudiofile/.libs/libaudiofile.a -o /work/fuzzer
