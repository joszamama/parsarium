#!/bin/sh
set -eu
# The parser build stays in build.sh so the AFL++ overlay's compiler rewrite
# instruments Ghostscript itself, not only the C++ harness.
cd /work/source
./configure CC=clang --without-x --disable-gtk --disable-cups --disable-dbus --disable-fontconfig \
  --without-tesseract --without-libpaper --without-libidn --without-ijs \
  --without-pcl --without-xps --without-gpdl --with-drivers=FILES
make -j 6 so-only XCFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' XLDFLAGS='-fprofile-instr-generate'
# Stage the public header at its installed path so the wrapper keeps the adapter's <ghostscript/iapi.h>.
mkdir -p /work/include/ghostscript
cp /work/source/psi/iapi.h /work/include/ghostscript/iapi.h
cd /work
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -I/work/include -L/work/source/sobin -lgs -Wl,-rpath,/work/lib -Wl,-export-dynamic'
clang++ -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp $common -o /work/replay
clang++ -fsanitize=fuzzer,address,undefined /work/harness.cpp $common -o /work/fuzzer
