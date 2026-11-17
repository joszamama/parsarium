#!/bin/sh
set -eu
cd /work/source
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --prefix=/work/install --disable-shared --enable-static --disable-frontend
make -j 4
make install
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags lame) /work/harness.cpp /work/replay.cpp $(pkg-config --static --libs lame) -lmpg123 -lm -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags lame) /work/harness.cpp $(pkg-config --static --libs lame) -lmpg123 -lm -o /work/fuzzer
