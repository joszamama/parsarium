#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' cmake -S /work/source -B /work/zzip-build \
 -DBUILD_SHARED_LIBS=OFF -DBUILD_TESTS=OFF -DZZIPMMAPPED=OFF -DZZIPFSEEKO=OFF \
 -DZZIPWRAP=OFF -DZZIPSDL=OFF -DZZIPBINS=OFF -DZZIPTEST=OFF -DZZIPDOCS=OFF \
 -DCMAKE_BUILD_TYPE=Debug
cmake --build /work/zzip-build --target libzzip -j 2
common='-O1 -g -fno-omit-frame-pointer -I/work/source -I/work/zzip-build'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp /work/zzip-build/zzip/libzzip.a -lz -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness.cpp /work/zzip-build/zzip/libzzip.a -lz -o /work/fuzzer
