#!/bin/sh
set -eu
ccommon='-std=c11 -O1 -g -fno-omit-frame-pointer -D_GNU_SOURCE -I/work/source/src -I/work/include'
cxxcommon='-std=c++17 -O1 -g -fno-omit-frame-pointer -I/work/source/src -I/work/include'
sources='/work/source/src/http-parser.c /work/deps/asprintf/src/asprintf.c /work/deps/mindex/src/mindex.c /work/deps/strextra/src/strnstr.c /work/deps/buf/buf.c'
for source in $sources; do
    stem=$(basename "$source" .c)
    clang $ccommon -fprofile-instr-generate -fcoverage-mapping -c "$source" -o "/work/$stem-cov.o"
    clang $ccommon -fsanitize=fuzzer-no-link,address,undefined -c "$source" -o "/work/$stem-fuzz.o"
done
clang++ $cxxcommon -fprofile-instr-generate -fcoverage-mapping \
    /work/harness.cpp /work/replay.cpp /work/*-cov.o -o /work/replay
clang++ $cxxcommon -fsanitize=fuzzer,address,undefined \
    /work/harness.cpp /work/*-fuzz.o -o /work/fuzzer
