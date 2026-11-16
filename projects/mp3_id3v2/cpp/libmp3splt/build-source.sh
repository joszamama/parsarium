#!/bin/sh
set -eu
cd /work/source
CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --prefix=/work/install --disable-static --disable-ogg --disable-flac \
 --disable-pcre --disable-cutter --disable-doxygen_doc
make -j 6
make install
