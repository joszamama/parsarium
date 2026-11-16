#!/bin/sh
set -eu
src=/work/source
common='-O1 -g -fno-omit-frame-pointer'
cmake -S "$src" -B /work/cov-build -DCMAKE_INSTALL_PREFIX=/work/install \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_C_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" \
    -DBUILD_SHARED_LIBS=OFF
cmake --build /work/cov-build --target libmp4tag -j 2
clang $common -fprofile-instr-generate -fcoverage-mapping \
    -I/work/cov-build /work/harness.c /work/replay.c \
    /work/cov-build/libmp4tag.a -o /work/replay
cmake -S "$src" -B /work/fuzz-build -DCMAKE_INSTALL_PREFIX=/work/install \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_C_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" \
    -DBUILD_SHARED_LIBS=OFF
cmake --build /work/fuzz-build --target libmp4tag -j 2
clang $common -fsanitize=fuzzer,address,undefined -I/work/fuzz-build \
    /work/harness.c /work/fuzz-build/libmp4tag.a -o /work/fuzzer
