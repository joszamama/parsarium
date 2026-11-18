#!/bin/sh
set -eu
# Build OpenSP's parser library (libosp) as a static archive only: no NLS, HTTP storage manager,
# documentation or programs. The generic event API (ParserEventGeneratorKit) is part of libosp.
# The 2005 config.guess predates aarch64, so the build triplet is passed explicitly. The 2005 sources use
# C++98 access declarations, which clang rejects in C++11 and later, so libosp is built as gnu++98
# (Debian builds it with g++, which only warns); -D_REENTRANT as in Debian's rules.
cd /work/source
CC=clang CXX=clang++ CXXFLAGS='-std=gnu++98 -O1 -g -fno-omit-frame-pointer -D_REENTRANT -fprofile-instr-generate -fcoverage-mapping' \
 CFLAGS='-O1 -g -fno-omit-frame-pointer' \
 ./configure --build="$(uname -m)-unknown-linux-gnu" --disable-shared --enable-static --disable-nls --disable-http --disable-doc-build
make -j 4 -C lib libosp.la
common='-O1 -g -fno-omit-frame-pointer -DSP_MULTI_BYTE=1'
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping -I/work/source/generic \
  /work/harness.cpp /work/replay.cpp /work/source/lib/.libs/libosp.a -lpthread -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -I/work/source/generic \
  /work/harness.cpp /work/source/lib/.libs/libosp.a -lpthread -o /work/fuzzer
