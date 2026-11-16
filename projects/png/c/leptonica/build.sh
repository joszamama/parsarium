#!/bin/sh
set -eu
cd /work/source
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --prefix=/work/install --disable-shared --enable-static --without-jpeg --without-libtiff --without-libwebp --without-libwebpmux --without-libopenjpeg
make -j 4
make install
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags lept) /work/harness.c /work/replay.c $(pkg-config --static --libs lept) -lm -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags lept) /work/harness.c $(pkg-config --static --libs lept) -lm -o /work/fuzzer
