#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping  -I/work/pngle-src/src  -c /work/pngle-src/src/pngle.c -o /work/pngle-cov.o
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -I/work/pngle-src/src -c /work/pngle-src/src/miniz.c -o /work/miniz-cov.o
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer-no-link,address,undefined  -I/work/pngle-src/src  -c /work/pngle-src/src/pngle.c -o /work/pngle-fuzz.o
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer-no-link,address,undefined -I/work/pngle-src/src -c /work/pngle-src/src/miniz.c -o /work/miniz-fuzz.o
clang -std=c11 $common -fprofile-instr-generate -fcoverage-mapping \
  -I/work/pngle-src/src /work/harness.c /work/replay.c \
  /work/pngle-cov.o /work/miniz-cov.o -lm -o /work/replay
clang -std=c11 $common -fsanitize=fuzzer,address,undefined \
  -I/work/pngle-src/src /work/harness.c \
  /work/pngle-fuzz.o /work/miniz-fuzz.o -lm -o /work/fuzzer
