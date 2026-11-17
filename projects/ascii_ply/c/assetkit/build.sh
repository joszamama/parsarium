#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
cmake -S /work/source -B /work/build \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_C_FLAGS="$common" \
  -DAK_SHARED=OFF -DAK_STATIC=ON -DAK_BUILD_EXPORTERS=OFF \
  -DAK_BUILD_DECODER_SHIMS=OFF -DAK_BUILD_CLI=OFF -DAK_FETCH_DEPS=OFF \
  -DGIT_SUBMODULE=OFF
cmake --build /work/build --target assetkit -j 2

libs='/work/build/libassetkit.a /work/build/deps/ds/libds.a /work/build/libdeflate.a'
clang -std=c11 $common -I/work/source/include -c /work/harness.c -o /work/harness.o
clang -std=c11 $common -c /work/replay.c -o /work/replay.o
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o \
  $libs -lm -ldl -pthread -o /work/replay

clang -std=c11 $common -c /work/fuzz.c -o /work/fuzz.o
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o \
  $libs -lm -ldl -pthread -o /work/fuzzer
