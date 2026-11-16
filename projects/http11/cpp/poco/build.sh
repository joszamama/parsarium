#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
cmake -S /work/source -B /work/build -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DBUILD_SHARED_LIBS=OFF -DPOCO_MINIMAL_BUILD=ON -DENABLE_NET=ON \
  -DENABLE_TESTS=OFF -DENABLE_SAMPLES=OFF -DENABLE_FASTLOGGER=OFF
cmake --build /work/build --target Net -j 4

clang++ -std=c++17 -O1 -g -fno-omit-frame-pointer \
  -fprofile-instr-generate -fcoverage-mapping -fsanitize=address,undefined \
  -I/work/source/Net/include -I/work/source/Foundation/include \
  /work/harness.cpp /work/replay.cpp \
  /work/build/lib/libPocoNetd.a /work/build/lib/libPocoFoundationd.a \
  -pthread -o /work/replay
clang++ -std=c++17 -O1 -g -fno-omit-frame-pointer \
  -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer,address,undefined \
  -I/work/source/Net/include -I/work/source/Foundation/include \
  /work/harness.cpp /work/fuzz.cpp \
  /work/build/lib/libPocoNetd.a /work/build/lib/libPocoFoundationd.a \
  -pthread -o /work/fuzzer
