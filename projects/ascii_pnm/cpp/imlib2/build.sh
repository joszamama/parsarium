#!/bin/sh
set -eu
cd /work/source
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --prefix=/work/install --without-x --without-jpeg --without-gif --without-svg --without-tiff --without-webp --without-heif --without-avif --without-jxl --without-j2k --without-raw --without-bz2 --without-lzma --without-id3 --without-ps
make -j 4
make install
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping -I/work/install/include /work/harness.cpp /work/replay.cpp -L/work/install/lib -lImlib2 -Wl,-rpath,/work/install/lib -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined -I/work/install/include /work/harness.cpp -L/work/install/lib -lImlib2 -Wl,-rpath,/work/install/lib -o /work/fuzzer
