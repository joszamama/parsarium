#!/bin/sh
set -eu

src=/work/sqlite-3.54.1
common='-O1 -g -fno-omit-frame-pointer -DSQLITE_CORE -DSQLITE_THREADSAFE=0'

cd "$src"
./configure --disable-shared
make sqlite3.c -j2
cd /work

clang $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
  -c "$src/sqlite3.c" -o /work/sqlite-coverage.o
clang $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
  -c "$src/ext/misc/zipfile.c" -o /work/zipfile-coverage.o
clang $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
  -c /work/harness.c -o /work/harness-coverage.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  /work/replay.cpp /work/harness-coverage.o /work/sqlite-coverage.o \
  /work/zipfile-coverage.o -lz -lm -o /work/replay

clang $common -fsanitize=fuzzer-no-link,address,undefined -I"$src" \
  -c "$src/sqlite3.c" -o /work/sqlite-fuzz.o
clang $common -fsanitize=fuzzer-no-link,address,undefined -I"$src" \
  -c "$src/ext/misc/zipfile.c" -o /work/zipfile-fuzz.o
clang $common -fsanitize=fuzzer-no-link,address,undefined -I"$src" \
  -c /work/harness.c -o /work/harness-fuzz.o
clang++ -O1 -g -fsanitize=fuzzer,address,undefined \
  /work/fuzz.cpp /work/harness-fuzz.o /work/sqlite-fuzz.o \
  /work/zipfile-fuzz.o -lz -lm -o /work/fuzzer
