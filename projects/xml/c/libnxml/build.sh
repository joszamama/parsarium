#!/bin/sh
set -eu
# libnxml's release tag has no generated configure; build out of tree.
cd /work/source
./autogen.sh
mkdir -p /work/build
cd /work/build
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
 /work/source/configure --disable-shared
make -j 4 -C src libnxml.la
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/build/src /work/harness.c /work/replay.c /work/build/src/.libs/libnxml.a -lcurl -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -fprofile-instr-generate -I/work/build/src /work/harness.c /work/build/src/.libs/libnxml.a -lcurl -o /work/fuzzer
