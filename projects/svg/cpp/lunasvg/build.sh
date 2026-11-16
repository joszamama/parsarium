#!/bin/sh
set -eu
CC=clang CXX=clang++ CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib -DBUILD_SHARED_LIBS=OFF -DLUNASVG_BUILD_EXAMPLES=OFF -DPLUTOVG_BUILD_EXAMPLES=OFF -DLUNASVG_DISABLE_LOAD_SYSTEM_FONTS=ON
cmake --build /work/build -j 4
cmake --install /work/build
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags lunasvg) /work/harness.cpp /work/replay.cpp $(pkg-config --static --libs lunasvg) -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags lunasvg) /work/harness.cpp $(pkg-config --static --libs lunasvg) -o /work/fuzzer
