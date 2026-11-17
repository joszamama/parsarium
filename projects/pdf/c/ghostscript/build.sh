#!/bin/sh
set -eu
# The parser build stays in build.sh so the AFL++ overlay's compiler rewrite
# instruments Ghostscript itself, not only the harness.
cd /work/source
./configure CC=clang --without-x --disable-gtk --disable-cups --disable-dbus --disable-fontconfig \
  --without-tesseract --without-libpaper --without-libidn --without-ijs \
  --without-pcl --without-xps --without-gpdl --with-drivers=FILES
make -j 6 so-only XCFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' XLDFLAGS='-fprofile-instr-generate'
cd /work
common='-O1 -g -fno-omit-frame-pointer -I/work/source/psi -L/work/source/sobin -lgs -Wl,-rpath,/work/lib -Wl,-export-dynamic'
clang -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c $common -o /work/replay
clang -fsanitize=fuzzer,address,undefined /work/harness.c $common -o /work/fuzzer
