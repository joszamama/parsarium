#!/bin/sh
set -eu

src=/work/sqlite-3.54.1
common='-O1 -g -fno-omit-frame-pointer -DSQLITE_CORE -DSQLITE_THREADSAFE=0'

cd "$src"
./configure --disable-shared
make sqlite3.c -j2
cd /work

clang $common -fprofile-instr-generate -fcoverage-mapping \
  -I"$src" /work/harness.c /work/replay.c \
  "$src/sqlite3.c" "$src/ext/misc/zipfile.c" -lz -lm -o /work/replay

clang $common -fsanitize=fuzzer,address,undefined \
  -I"$src" /work/harness.c \
  "$src/sqlite3.c" "$src/ext/misc/zipfile.c" -lz -lm -o /work/fuzzer
