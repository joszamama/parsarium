#!/bin/sh
set -eu

src=/work/libzip-1.12.1
common='-O1 -g -fno-omit-frame-pointer'
options='-DBUILD_SHARED_LIBS=OFF -DBUILD_TOOLS=OFF -DBUILD_REGRESS=OFF -DBUILD_OSSFUZZ=OFF -DBUILD_EXAMPLES=OFF -DBUILD_DOC=OFF -DENABLE_COMMONCRYPTO=OFF -DENABLE_GNUTLS=OFF -DENABLE_OPENSSL=OFF -DENABLE_BZIP2=OFF -DENABLE_LZMA=OFF -DENABLE_ZSTD=OFF'

cmake -S "$src" -B /work/coverage-build \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" \
  $options
cmake --build /work/coverage-build --target zip -j 2
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping \
  -I"$src/lib" -I/work/coverage-build /work/harness.cpp /work/replay.cpp \
  /work/coverage-build/lib/libzip.a -lz -o /work/replay

cmake -S "$src" -B /work/fuzz-build \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" \
  $options
cmake --build /work/fuzz-build --target zip -j 2
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined \
  -I"$src/lib" -I/work/fuzz-build /work/harness.cpp \
  /work/fuzz-build/lib/libzip.a -lz -o /work/fuzzer
