#!/bin/sh
set -eu

# Poco Foundation links its bundled zlib 1.3.2 (dependencies/zlib/src) as an
# object library, so the same coverage flags instrument zlib inflate.
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
cmake -S /work/source -B /work/build -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DBUILD_SHARED_LIBS=OFF -DPOCO_MINIMAL_BUILD=ON -DPOCO_UNBUNDLED=OFF -DENABLE_ZIP=ON \
  -DENABLE_TESTS=OFF -DENABLE_SAMPLES=OFF -DENABLE_FASTLOGGER=OFF
cmake --build /work/build --target Zip -j 4

clang++ -std=c++17 -O1 -g -fno-omit-frame-pointer \
  -fprofile-instr-generate -fcoverage-mapping -fsanitize=address,undefined \
  -I/work/source/Zip/include -I/work/source/Foundation/include \
  /work/harness.cpp /work/replay.cpp \
  /work/build/lib/libPocoZipd.a /work/build/lib/libPocoFoundationd.a \
  -pthread -o /work/replay
clang++ -std=c++17 -O1 -g -fno-omit-frame-pointer \
  -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer,address,undefined \
  -I/work/source/Zip/include -I/work/source/Foundation/include \
  /work/harness.cpp /work/fuzz.cpp \
  /work/build/lib/libPocoZipd.a /work/build/lib/libPocoFoundationd.a \
  -pthread -o /work/fuzzer
