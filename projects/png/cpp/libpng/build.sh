#!/bin/sh
set -eu

src=/work/libpng-1.6.59
common='-O1 -g -fno-omit-frame-pointer'

cmake -S "$src" -B /work/coverage-build \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" \
  -DPNG_SHARED=OFF -DPNG_STATIC=ON -DPNG_TESTS=OFF
cmake --build /work/coverage-build --target png_static -j 2
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping \
  -I"$src" -I/work/coverage-build /work/harness.cpp /work/replay.cpp \
  /work/coverage-build/libpng16.a -lz -lm -o /work/replay

cmake -S "$src" -B /work/fuzz-build \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" \
  -DPNG_SHARED=OFF -DPNG_STATIC=ON -DPNG_TESTS=OFF
cmake --build /work/fuzz-build --target png_static -j 2
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined \
  -I"$src" -I/work/fuzz-build /work/harness.cpp \
  /work/fuzz-build/libpng16.a -lz -lm -o /work/fuzzer
