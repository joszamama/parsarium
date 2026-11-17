#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
cmake -S /work/source -B /work/assimp-build \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DBUILD_SHARED_LIBS=OFF -DASSIMP_BUILD_TESTS=OFF \
  -DASSIMP_BUILD_ASSIMP_TOOLS=OFF -DASSIMP_BUILD_SAMPLES=OFF \
  -DASSIMP_NO_EXPORT=ON -DASSIMP_BUILD_ALL_IMPORTERS_BY_DEFAULT=OFF \
  -DASSIMP_BUILD_PLY_IMPORTER=ON -DASSIMP_BUILD_ZLIB=OFF \
  -DASSIMP_BUILD_MINIZIP=ON -DASSIMP_WARNINGS_AS_ERRORS=OFF \
  -DASSIMP_IGNORE_GIT_HASH=ON -DASSIMP_INJECT_DEBUG_POSTFIX=OFF
cmake --build /work/assimp-build --target assimp -j 2

clang -std=c11 $common -I/work/source/include -I/work/assimp-build/include \
  -c /work/harness.c -o /work/harness.o
clang -std=c11 $common -c /work/replay.c -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o \
  /work/assimp-build/lib/libassimp.a -lz -ldl -o /work/replay

clang -std=c11 $common -c /work/fuzz.c -o /work/fuzz.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o \
  /work/assimp-build/lib/libassimp.a -lz -ldl -o /work/fuzzer
