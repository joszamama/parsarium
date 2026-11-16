#!/bin/sh
set -eu
cp /work/source/config.mk.in /work/source/config.mk
cp -a /work/source /work/source-fuzz
make -C /work/source lib/all NETPBMLIBTYPE=unixstatic CC=clang \
  CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  CFLAGS_FOR_BUILD='-O1 -g' -j1
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping -I/work/source/lib/importinc -I/work/source/lib/util/importinc \
  /work/harness.c /work/replay.c /work/source/lib/libnetpbm.a -lm -o /work/replay
make -C /work/source-fuzz lib/all NETPBMLIBTYPE=unixstatic CC=clang \
  CFLAGS='-O1 -g -fsanitize=fuzzer-no-link,address,undefined' \
  CFLAGS_FOR_BUILD='-O1 -g' -j1
clang -O1 -g -fsanitize=fuzzer,address,undefined -I/work/source-fuzz/lib/importinc -I/work/source-fuzz/lib/util/importinc \
  /work/harness.c /work/source-fuzz/lib/libnetpbm.a -lm -o /work/fuzzer
