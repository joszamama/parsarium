#!/bin/sh
set -eu
src=/work/rply-1.1.4
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
  -c "$src/rply.c" -o /work/parser-coverage.o
clang $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
  /work/harness.c /work/replay.c /work/parser-coverage.o -lm -o /work/replay
clang $common -fsanitize=fuzzer-no-link,address,undefined -I"$src" \
  -c "$src/rply.c" -o /work/parser-fuzz.o
clang $common -fsanitize=fuzzer,address,undefined -I"$src" \
  /work/harness.c /work/parser-fuzz.o -lm -o /work/fuzzer
