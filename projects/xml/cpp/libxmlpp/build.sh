#!/bin/sh
set -eu

export AFL_LLVM_INSTRUMENT=CLASSIC
export CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
export CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
export LDFLAGS='-fprofile-instr-generate'

cd /work/libxml2-source
CC=clang ./configure --prefix=/opt/libxml2 --libdir=/opt/libxml2/lib \
  --disable-shared --enable-static --without-python --without-zlib \
  --without-lzma --without-iconv --without-icu --without-http --without-debug
make -j8
make install

export PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig
CC=clang CXX=clang++ meson setup /work/libxmlpp-build /work/source \
  --prefix=/opt/libxmlpp --libdir=lib -Ddefault_library=static \
  -Dmaintainer-mode=false -Dbuild-documentation=false \
  -Dbuild-examples=false -Dbuild-tests=false
meson compile -C /work/libxmlpp-build -j8
meson install -C /work/libxmlpp-build

export PKG_CONFIG_PATH=/opt/libxmlpp/lib/pkgconfig:/opt/libxml2/lib/pkgconfig
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
clang++ $common -I/work /work/harness.cpp /work/replay.cpp \
  $(pkg-config --cflags --libs --static libxml++-5.0) -o /work/replay
clang++ $common -fsanitize=fuzzer,address -I/work /work/harness.cpp \
  $(pkg-config --cflags --libs --static libxml++-5.0) -o /work/fuzzer
clang++ $common /work/parser-probe.cpp \
  $(pkg-config --cflags --libs --static libxml++-5.0) -o /work/parser-probe
