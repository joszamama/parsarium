#!/bin/sh
set -eu
cd /work/source
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 ./configure --disable-shared --enable-static --disable-gtk-doc --without-gdk-pixbuf --disable-nls
make -j 4
common="-O1 -g -fno-omit-frame-pointer -I/work/source $(pkg-config --cflags glib-2.0 gobject-2.0 gio-2.0 libxml-2.0)"
libs="/work/source/gsf/.libs/libgsf-1.a $(pkg-config --libs glib-2.0 gobject-2.0 gio-2.0 libxml-2.0) -lz"
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp $libs -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness.cpp $libs -o /work/fuzzer
