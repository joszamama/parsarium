#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
cmake -S /work/source -B /work/cov-build -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" \
  -DBUILD_SHARED_LIBS=OFF -DBUILD_TESTING=OFF
cmake --build /work/cov-build --target miniz -j 2
clang $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/source -I/work/cov-build /work/harness.c /work/replay.c \
  /work/cov-build/libminiz.a -lm -o /work/replay
cmake -S /work/source -B /work/fuzz-build -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" \
  -DBUILD_SHARED_LIBS=OFF -DBUILD_TESTING=OFF
cmake --build /work/fuzz-build --target miniz -j 2
clang $common -fsanitize=fuzzer,address,undefined \
  -I/work/source -I/work/fuzz-build /work/harness.c \
  /work/fuzz-build/libminiz.a -lm -o /work/fuzzer
