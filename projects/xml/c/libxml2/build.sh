#!/bin/sh
set -eu
cd /work/source
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --prefix=/work/install --disable-shared --enable-static --without-python --without-zlib --without-lzma --without-iconv --without-icu --without-http --without-modules --without-threads --without-catalog
make -j 4
make install
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags libxml-2.0) /work/harness.c /work/replay.c $(pkg-config --static --libs libxml-2.0) -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags libxml-2.0) /work/harness.c $(pkg-config --static --libs libxml-2.0) -o /work/fuzzer
