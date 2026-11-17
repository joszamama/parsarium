#!/bin/sh
set -eu

# One libmicrohttpd build carries LLVM source coverage for replay and sanitizer
# coverage for the fuzzer, so both binaries exercise instrumented MHD code.
# The out-of-tree build keeps absolute /work/source paths in coverage data.
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
mkdir -p /work/mhd-build
cd /work/mhd-build
CC=clang CFLAGS="$common" LDFLAGS="$common" /work/source/configure \
  --enable-static --disable-shared --disable-https --without-gnutls \
  --disable-curl --disable-doc --disable-examples --disable-tools
make -C src/microhttpd -j 4 libmicrohttpd.la
cd /work

mhd='/work/mhd-build/src/microhttpd/.libs/libmicrohttpd.a'
mhd_includes='-I/work/source/src/include'

clang++ -std=c++17 $common $mhd_includes -c /work/harness.cpp -o /work/harness.o
clang++ -std=c++17 $common -c /work/replay.cpp -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o "$mhd" -pthread -o /work/replay

clang++ -std=c++17 $common -c /work/fuzz.cpp -o /work/fuzz.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o "$mhd" -pthread -o /work/fuzzer
