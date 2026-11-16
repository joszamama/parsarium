#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib -DBUILD_SHARED_LIBS=OFF -DEXAMPLE=OFF -DASO=OFF
cmake --build /work/build -j 4
cmake --install /work/build
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags mad) /work/harness.c /work/replay.c $(pkg-config --static --libs mad) -lm -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags mad) /work/harness.c $(pkg-config --static --libs mad) -lm -o /work/fuzzer
