#!/bin/sh
set -eu
src=/work/source
common='-O1 -g -fno-omit-frame-pointer'
make -C "$src" CC=clang BUILDDIR=/work/cov-build \
    CFLAGS="$common -fprofile-instr-generate -fcoverage-mapping" lib
clang $common -fprofile-instr-generate -fcoverage-mapping \
    -I/work/source/include /work/harness.c /work/replay.c \
    /work/cov-build/libtspdf.a -lm -o /work/replay
make -C "$src" CC=clang BUILDDIR=/work/fuzz-build \
    CFLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" lib
clang $common -fsanitize=fuzzer,address,undefined -I/work/source/include \
    /work/harness.c /work/fuzz-build/libtspdf.a -lm -o /work/fuzzer
