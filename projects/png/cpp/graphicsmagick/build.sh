#!/bin/sh
set -eu
cd /work/source
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --prefix=/work/install --disable-shared --enable-static --disable-openmp \
 --without-x --without-magick-plus-plus --without-modules --with-quantum-depth=8  \
 --with-png=yes --without-xml --without-lcms --without-freetype
make -j 4
make install
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags GraphicsMagickWand) /work/harness.cpp /work/replay.cpp $(pkg-config --static --libs GraphicsMagickWand) -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags GraphicsMagickWand) /work/harness.cpp $(pkg-config --static --libs GraphicsMagickWand) -o /work/fuzzer
