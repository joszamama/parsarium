#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' cmake -S /work/source -B /work/unarr-build \
 -DBUILD_SHARED_LIBS=OFF -DCMAKE_BUILD_TYPE=Debug -DENABLE_7Z=OFF \
 -DUSE_SYSTEM_BZ2=OFF -DUSE_SYSTEM_LZMA=OFF -DUSE_SYSTEM_ZLIB=ON
cmake --build /work/unarr-build --target unarr -j 2
common='-O1 -g -fno-omit-frame-pointer -I/work/unarr-build'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp /work/unarr-build/libunarr.a -lz -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness.cpp /work/unarr-build/libunarr.a -lz -o /work/fuzzer
