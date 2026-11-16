#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/archive-build -DBUILD_SHARED_LIBS=OFF \
 -DENABLE_TEST=OFF -DENABLE_TAR=OFF -DENABLE_CPIO=OFF -DENABLE_CAT=OFF \
 -DENABLE_OPENSSL=OFF -DENABLE_LIBB2=OFF -DENABLE_LZ4=OFF -DENABLE_LZMA=OFF \
 -DENABLE_ZSTD=OFF -DENABLE_LIBXML2=OFF -DENABLE_EXPAT=OFF -DENABLE_ICONV=OFF \
 -DENABLE_XATTR=OFF -DENABLE_ZLIB=ON
cmake --build /work/archive-build --target archive_static -j 4
common='-O1 -g -fno-omit-frame-pointer -I/work/source/libarchive -I/work/archive-build'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp /work/archive-build/libarchive/libarchive.a -lz -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness.cpp /work/archive-build/libarchive/libarchive.a -lz -o /work/fuzzer
