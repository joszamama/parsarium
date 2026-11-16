#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/build -DBUILD_SHARED_LIBS=OFF
cmake --build /work/build --target id3tag -j 4
library=$(find /work/build -name libid3tag.a -print -quit)
test -n "$library"
common='-O1 -g -fno-omit-frame-pointer -I/work/build -I/work/source/src'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c "$library" -lz -lm -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c "$library" -lz -lm -o /work/fuzzer
