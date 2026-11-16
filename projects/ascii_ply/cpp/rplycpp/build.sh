#!/bin/sh
set -eu
CC=clang CXX=clang++ CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib -DBUILD_SHARED_LIBS=OFF -DRPLYCPP_BUILD_TESTS=OFF -DRPLYCPP_BUILD_SAMPLES=OFF
cmake --build /work/build -j 4
cmake --install /work/build
common='-O1 -g -fno-omit-frame-pointer -std=c++17'
clang++ $common -fprofile-instr-generate -fcoverage-mapping -I/work/source/src -I/work/source/third_party/rply /work/harness.cpp /work/replay.cpp /work/install/lib/librplycpp.a -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined -I/work/source/src -I/work/source/third_party/rply /work/harness.cpp /work/install/lib/librplycpp.a -o /work/fuzzer
