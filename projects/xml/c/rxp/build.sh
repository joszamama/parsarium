#!/bin/sh
set -eu
# Debian's rxp 1.5.0-3.1 patches (LP64 fixes, automake library build) are applied to the orig tarball.
# The library sources are librxp_la_SOURCES from the patched Makefile.am, compiled directly with the
# same -DCHAR_SIZE=16 and include paths; the rxp command-line program (src/rxp.c) is not built.
cd /work/source
for patch in $(cat /work/debian/patches/series); do patch -p1 < "/work/debian/patches/$patch"; done
# configure only generates config.h (PACKAGE_VERSION and HAVE_* macros); the 2013 config.guess predates
# aarch64, so the build triplet is passed explicitly.
CC=clang ./configure --build="$(uname -m)-unknown-linux-gnu" --disable-shared > /dev/null
lib="src/charset.c src/ctype16.c src/dtd.c src/hash.c src/http.c src/infoset-print.c src/input.c src/namespaces.c src/nf16check.c src/nf16data.c src/stdio16.c src/string16.c src/system.c src/url.c src/version.c src/xmlparser.c catalog/catalog.c catalog/catalog_dtd.c catalog/catutil.c catalog/entityopener.c catalog/resolve.c"
flags='-DHAVE_CONFIG_H -I/work/source -DCHAR_SIZE=16 -I/work/source/include -I/work/source/catalog -O1 -g -fno-omit-frame-pointer -w'
mkdir -p /work/obj
for src in $lib; do
  clang $flags -fprofile-instr-generate -fcoverage-mapping -c "/work/source/$src" -o "/work/obj/$(echo "$src" | tr / _).o"
done
ar rcs /work/librxp.a /work/obj/*.o
common='-DHAVE_CONFIG_H -I/work/source -DCHAR_SIZE=16 -I/work/source/include -I/work/source/catalog -O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c /work/librxp.a -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c /work/librxp.a -o /work/fuzzer
