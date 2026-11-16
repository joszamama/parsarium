#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' cmake -S /work/source -B /work/mz-build \
 -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Debug -DMZ_ZLIB=ON -DMZ_BZIP2=OFF \
 -DMZ_LZMA=OFF -DMZ_ZSTD=OFF -DMZ_OPENSSL=OFF -DMZ_LIBCOMP=OFF -DMZ_PPMD=OFF \
 -DMZ_COMPAT=OFF -DMZ_BUILD_TESTS=OFF -DMZ_BUILD_UNIT_TESTS=OFF
cmake --build /work/mz-build --target minizip-ng -j 2
common='-O1 -g -fno-omit-frame-pointer -I/work/source -I/work/mz-build'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp /work/mz-build/libminizip-ng.a -lz -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness.cpp /work/mz-build/libminizip-ng.a -lz -o /work/fuzzer
