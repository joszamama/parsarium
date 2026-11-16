#!/bin/sh
set -eu
mkdir -p /work/source/compat
printf '#include <iomanip>\n' > /work/source/compat/iomanip.h
cd /work/source
CPPFLAGS='-I/work/source/compat' CC=clang CXX=clang++ \
 CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
 CXXFLAGS='-O1 -g -std=gnu++14 -include cstring -include cstdlib -include cstdio -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --build=aarch64-unknown-linux-gnu --prefix=/work/install --disable-static
sed -i 's/^SUBDIRS = .*/SUBDIRS = include src/' Makefile
make -j 6
make install
# Bundled libtool omits Clang's profiling runtime when linking this DSO.
clang++ -shared -fprofile-instr-generate -fcoverage-mapping /work/source/src/*.lo \
 -Wl,-soname,libid3-3.8.so.3 -lz -o /work/install/lib/libid3-3.8.so.3.0.0
