#!/bin/sh
set -eu
src=/work/llhttp-9.4.3
common='-O1 -g -fno-omit-frame-pointer'
for unit in "$src/build/c/llhttp.c" "$src/src/native/api.c" "$src/src/native/http.c"; do
  name=$(basename "$unit" .c)
  clang $common -fprofile-instr-generate -fcoverage-mapping -I"$src/build" \
    -c "$unit" -o /work/$name-cov.o
  clang $common -fsanitize=fuzzer-no-link,address,undefined -I"$src/build" \
    -c "$unit" -o /work/$name-fuzz.o
done
clang $common -fprofile-instr-generate -fcoverage-mapping -I"$src/build" \
  /work/harness.c /work/replay.c /work/*-cov.o -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -I"$src/build" \
  /work/harness.c /work/*-fuzz.o -o /work/fuzzer
