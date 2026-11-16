#!/bin/sh
set -eu
common='-std=c11 -O1 -g -fno-omit-frame-pointer -D_GNU_SOURCE -I/work/source/src -I/work/include'
sources='/work/source/src/http-parser.c /work/deps/asprintf/src/asprintf.c /work/deps/mindex/src/mindex.c /work/deps/strextra/src/strnstr.c /work/deps/buf/buf.c'
clang $common -fprofile-instr-generate -fcoverage-mapping \
    /work/harness.c /work/replay.c $sources -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined \
    /work/harness.c $sources -o /work/fuzzer
