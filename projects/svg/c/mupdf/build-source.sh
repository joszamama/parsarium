#!/bin/sh
set -eu
cd /work/source
make -j 6 libs CC=clang CXX=clang++ shared=yes build=release \
  USE_SYSTEM_CURL=no USE_TESSERACT=no USE_ZXINGCPP=no USE_LEPTONICA=no \
  XCFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  XLDFLAGS='-fprofile-instr-generate'
