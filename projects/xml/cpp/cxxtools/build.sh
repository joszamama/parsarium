#!/bin/sh
set -eu
# Build cxxtools as a static library (no SSL, demos or unit tests); its XML reader is part of libcxxtools.
# tcpsocketimpl.h includes <openssl/ssl.h> even --without-ssl, so the build stage has libssl-dev headers only.
# timer.cpp uses struct tm without <ctime>, which current libstdc++ no longer pulls in; force-include it.
cd /work/source
CC=clang CXX=clang++ CXXFLAGS='-O1 -g -fno-omit-frame-pointer -include ctime -fprofile-instr-generate -fcoverage-mapping' \
 CFLAGS='-O1 -g -fno-omit-frame-pointer' LDFLAGS='-fprofile-instr-generate' \
 ./configure --disable-shared --enable-static --without-ssl --disable-demos --disable-unittest
make -j 4 -C src libcxxtools.la
common='-O1 -g -fno-omit-frame-pointer'
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping -I/work/source/include \
  /work/harness.cpp /work/replay.cpp /work/source/src/.libs/libcxxtools.a -lpthread -ldl -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -I/work/source/include \
  /work/harness.cpp /work/source/src/.libs/libcxxtools.a -lpthread -ldl -o /work/fuzzer
