#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/raylib-build -DPLATFORM=Memory -DBUILD_EXAMPLES=OFF -DBUILD_SHARED_LIBS=OFF
cmake --build /work/raylib-build --target raylib -j 4
common='-O1 -g -fno-omit-frame-pointer -I/work/source/src'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c /work/raylib-build/raylib/libraylib.a -lm -ldl -lpthread -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c /work/raylib-build/raylib/libraylib.a -lm -ldl -lpthread -o /work/fuzzer
