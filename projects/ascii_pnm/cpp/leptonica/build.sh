#!/bin/sh
set -eu

src=/work/leptonica-1.87.0
common='-O1 -g -fno-omit-frame-pointer'
options='-DBUILD_SHARED_LIBS=OFF -DBUILD_PROG=OFF -DSW_BUILD=OFF -DENABLE_ZLIB=OFF -DENABLE_PNG=OFF -DENABLE_GIF=OFF -DENABLE_JPEG=OFF -DENABLE_TIFF=OFF -DENABLE_WEBP=OFF -DENABLE_OPENJPEG=OFF'

cmake -S "$src" -B /work/coverage-build \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" \
  $options
cmake --build /work/coverage-build --target leptonica -j 2
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping \
  -I"$src/src" -I/work/coverage-build/src /work/harness.cpp /work/replay.cpp \
  /work/coverage-build/src/libleptonica.a -lm -o /work/replay

cmake -S "$src" -B /work/fuzz-build \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" \
  $options
cmake --build /work/fuzz-build --target leptonica -j 2
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined \
  -I"$src/src" -I/work/fuzz-build/src /work/harness.cpp \
  /work/fuzz-build/src/libleptonica.a -lm -o /work/fuzzer
