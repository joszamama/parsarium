#!/bin/sh
set -eu

# Same pinned, minimal libmicrohttpd build as projects/http11/cpp/libmicrohttpd:
# one static library carries LLVM source coverage for replay and sanitizer
# coverage for the fuzzer, so both binaries exercise instrumented MHD code.
# The out-of-tree build keeps absolute /work/source paths in coverage data.
# The harness is C11 with GNU extensions for socket and fork APIs.
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

clang -std=gnu11 -Wall -Wextra $common $mhd_includes -c /work/harness.c -o /work/harness.o
clang -std=gnu11 -Wall -Wextra $common -c /work/replay.c -o /work/replay.o
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o "$mhd" -pthread -o /work/replay

clang -std=gnu11 -Wall -Wextra $common -c /work/fuzz.c -o /work/fuzz.o
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o "$mhd" -pthread -o /work/fuzzer
