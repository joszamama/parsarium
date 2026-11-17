#!/bin/sh
set -eu
cd /work/source
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --prefix=/work/install --disable-shared --enable-static --disable-openmp \
 --without-libltdl --without-magic --without-png --without-lame --without-twolame \
 --without-oggvorbis --without-flac --without-sndfile --with-mad=yes --with-id3tag=yes --with-mp3=yes
make -j 4
make install
library=$(find /work/source -name libsox.a -print -quit)
test -n "$library"
common='-O1 -g -fno-omit-frame-pointer -I/work/source/src'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c "$library" -lmad -lid3tag -lz -lm -lpthread -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c "$library" -lmad -lid3tag -lz -lm -lpthread -o /work/fuzzer
