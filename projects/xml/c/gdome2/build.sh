#!/bin/sh
set -eu
# libxml2 from the pinned release (static, out of tree) is the parser gdome2 builds its DOM on, as Debian links libgdome2-0 to libxml2.
cov='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
mkdir -p /work/libxml2-build
cd /work/libxml2-build
CC=clang CFLAGS="$cov" LDFLAGS='-fprofile-instr-generate' /work/libxml2-source/configure --prefix=/work/prefix --libdir=/work/prefix/lib \
 --disable-shared --enable-static --without-python --without-zlib --without-lzma --without-iconv --without-icu --without-http --without-debug
make -j 4
make install
# gdome2's library sources (Debian 0.8.1+debian-10 with its two source patches) are compiled directly into a static
# archive: the 2003 autotools files need Debian's configure rewrite, and config.h holds only STDC_HEADERS and DEBUG_REFCNT.
printf '#define STDC_HEADERS 1\n#define DEBUG_REFCNT 0\n' > /work/source/config.h
xml=$(PKG_CONFIG_PATH=/work/prefix/lib/pkgconfig pkg-config --cflags libxml-2.0)
glib=$(pkg-config --cflags glib-2.0)
inc="-I/work/source -I/work/source/libgdome -I/work/source/libgdome/gdomecore -I/work/source/libgdome/events -I/work/source/libgdome/xpath $xml $glib"
mkdir -p /work/gdome-obj
for f in /work/source/libgdome/*.c /work/source/libgdome/gdomecore/*.c /work/source/libgdome/events/*.c /work/source/libgdome/xpath/*.c; do
  clang $cov -std=gnu89 -DHAVE_CONFIG_H -Wno-deprecated-declarations -Wno-int-conversion -Wno-incompatible-pointer-types \
    -Wno-implicit-function-declaration $inc -c "$f" -o "/work/gdome-obj/$(basename "$f" .c).o"
done
ar rcs /work/libgdome.a /work/gdome-obj/*.o
common='-O1 -g -fno-omit-frame-pointer'
libs="/work/libgdome.a $(PKG_CONFIG_PATH=/work/prefix/lib/pkgconfig pkg-config --static --libs libxml-2.0) $(pkg-config --libs glib-2.0)"
clang $common -fprofile-instr-generate -fcoverage-mapping $inc /work/harness.c /work/replay.c $libs -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -fprofile-instr-generate $inc /work/harness.c $libs -o /work/fuzzer
