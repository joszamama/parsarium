#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping  -I/work/libspng-src/spng  -c /work/libspng-src/spng/spng.c -o /work/libspng-cov.o
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer-no-link,address,undefined  -I/work/libspng-src/spng  -c /work/libspng-src/spng/spng.c -o /work/libspng-fuzz.o
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/libspng-src/spng /work/harness.cpp /work/replay.cpp \
  /work/libspng-cov.o -lz -lm -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined \
  -I/work/libspng-src/spng /work/harness.cpp /work/libspng-fuzz.o \
  -lz -lm -o /work/fuzzer
