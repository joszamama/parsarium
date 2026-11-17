#!/bin/sh
set -eu
cd /work/source
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --prefix=/work/install --disable-shared --enable-static --without-docbook --without-xmlwf --without-examples --without-tests
make -j 4
make install
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags expat) /work/harness.c /work/replay.c $(pkg-config --static --libs expat) -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags expat) /work/harness.c $(pkg-config --static --libs expat) -o /work/fuzzer
