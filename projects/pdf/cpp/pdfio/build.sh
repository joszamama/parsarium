#!/bin/sh
set -eu
src=/work/pdfio-1.6.5
common='-O1 -g -fno-omit-frame-pointer'
cd "$src"
CC=clang CFLAGS="$common -fprofile-instr-generate -fcoverage-mapping" ./configure --prefix=/work/install
make libpdfio.a -j 2
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
 /work/harness.cpp /work/replay.cpp "$src/libpdfio.a" -lz -lm -o /work/replay
make clean
CC=clang CFLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" ./configure --prefix=/work/install
make libpdfio.a -j 2
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -I"$src" \
 /work/harness.cpp "$src/libpdfio.a" -lz -lm -o /work/fuzzer
