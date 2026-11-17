#!/bin/sh
set -eu

src=/work/OpenMesh-11.0.0
common='-O1 -g -fno-omit-frame-pointer'

cmake -S "$src" -B /work/coverage-build -DBUILD_APPS=OFF \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_STANDARD=17 \
  -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_CXX_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping"
cmake --build /work/coverage-build --target OpenMeshCoreStatic -j 2
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping \
  -I"$src/src" /work/harness.cpp /work/replay.cpp \
  -Wl,--whole-archive /work/coverage-build/Build/lib/libOpenMeshCore.a \
  -Wl,--no-whole-archive -o /work/replay

cmake -S "$src" -B /work/fuzz-build -DBUILD_APPS=OFF \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_STANDARD=17 \
  -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_CXX_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined"
cmake --build /work/fuzz-build --target OpenMeshCoreStatic -j 2
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined \
  -I"$src/src" /work/harness.cpp /work/fuzz.cpp \
  -Wl,--whole-archive /work/fuzz-build/Build/lib/libOpenMeshCore.a \
  -Wl,--no-whole-archive -o /work/fuzzer
