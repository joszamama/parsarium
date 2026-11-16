#!/bin/sh
set -eu
src=/work/zlib-1.4/contrib/minizip
common='-O1 -g -fno-omit-frame-pointer'
for unit in unzip ioapi; do
 clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/zlib-1.4 -I/work/zlib-1.4/contrib \
   -c "$src/$unit.c" -o /work/$unit-cov.o
 clang $common -fsanitize=fuzzer-no-link,address,undefined -I/work/zlib-1.4 -I/work/zlib-1.4/contrib \
   -c "$src/$unit.c" -o /work/$unit-fuzz.o
done
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping -I/work/zlib-1.4 -I/work/zlib-1.4/contrib \
 /work/harness.cpp /work/replay.cpp /work/*-cov.o -lz -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -I/work/zlib-1.4 -I/work/zlib-1.4/contrib \
 /work/harness.cpp /work/*-fuzz.o -lz -o /work/fuzzer
