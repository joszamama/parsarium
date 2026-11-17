#!/bin/sh
set -eu
# CMake's host FPU probe reports false under linux/arm64 emulation, while
# AArch64 guarantees floating point and the selected NEON decoder requires it.
sed -i 's/cmake_host_system_information(RESULT HAVE_FPU QUERY HAS_FPU)/set(HAVE_FPU 1)/' /work/source/ports/cmake/src/CMakeLists.txt
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source/ports/cmake -B /work/build -DBUILD_SHARED_LIBS=OFF -DBUILD_LIBOUT123=OFF
cmake --build /work/build --target libmpg123 -j 4
library=$(find /work/build -name libmpg123.a -print -quit)
test -n "$library"
common='-O1 -g -fno-omit-frame-pointer -I/work/source/src/include'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp "$library" -lm -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness.cpp "$library" -lm -o /work/fuzzer
