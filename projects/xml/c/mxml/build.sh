#!/bin/sh
set -eu
cd /work/source
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
 ./configure --disable-shared --disable-threads
make -j 4 libmxml4.a
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/source /work/harness.c /work/replay.c /work/source/libmxml4.a -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -fprofile-instr-generate -I/work/source /work/harness.c /work/source/libmxml4.a -o /work/fuzzer
