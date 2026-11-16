#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping  -I/work/pngle-src/src  -c /work/pngle-src/src/pngle.c -o /work/pngle-cov.o
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -I/work/pngle-src/src -c /work/pngle-src/src/miniz.c -o /work/miniz-cov.o
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer-no-link,address,undefined  -I/work/pngle-src/src  -c /work/pngle-src/src/pngle.c -o /work/pngle-fuzz.o
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer-no-link,address,undefined -I/work/pngle-src/src -c /work/pngle-src/src/miniz.c -o /work/miniz-fuzz.o
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/pngle-src/src /work/harness.cpp /work/replay.cpp \
  /work/pngle-cov.o /work/miniz-cov.o -lm -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined \
  -I/work/pngle-src/src /work/harness.cpp \
  /work/pngle-fuzz.o /work/miniz-fuzz.o -lm -o /work/fuzzer
