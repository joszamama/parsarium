#!/bin/sh
set -eu
mkdir -p /work/generated
cp /work/source/interoff-lib.c /work/generated/interoff-lib.c
# McStas expands this directive when generating an instrument. The library's
# PLY parser remains byte-for-byte the tagged upstream C source.
sed '/^%include "read_table-lib"$/d' /work/source/interoff-lib.h > /work/generated/interoff-lib.h
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -Wno-unknown-pragmas'
clang -std=gnu11 $common -include /work/compat.h -I/work/generated \
  -c /work/generated/interoff-lib.c -o /work/interoff-lib.o
clang -std=gnu11 $common -include /work/compat.h -I/work/generated \
  -c /work/harness.c -o /work/harness.o
clang -std=gnu11 $common /work/interoff-lib.o /work/harness.o /work/replay.c \
  -lm -o /work/replay
clang -std=gnu11 $common /work/interoff-lib.o /work/harness.o /work/fuzz.c \
  -lm -o /work/fuzzer
