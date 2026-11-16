#!/bin/sh
set -eu
cd /work/source
CC=clang CXX=clang++ CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --prefix=/work/install --disable-shared --enable-static --disable-openmp \
 --without-x --with-magick-plus-plus --without-modules --with-quantum-depth=8 --disable-hdri \
 --with-png=yes --with-xml=yes --without-lcms --without-freetype
make -j 4
make install
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags Magick++) /work/harness.cpp /work/replay.cpp $(pkg-config --static --libs Magick++) -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags Magick++) /work/harness.cpp $(pkg-config --static --libs Magick++) -o /work/fuzzer
