#!/bin/sh
set -eu
# Debian's libcutl 1.10.0+ds1 drops the bundled Expat subset and builds with --with-external-expat;
# do the same against the pinned Expat 2.10.0 (the C XML cell's release), built static.
cov='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
cd /work/expat-source
CC=clang CFLAGS="$cov" ./configure --prefix=/work/expat --disable-shared --enable-static \
  --without-docbook --without-xmlwf --without-examples --without-tests
make -j 4
make install
# Only libcutl's XML parser component is compiled (cutl/xml/*.cxx and the exception base); the
# library's other components (regular expressions over Boost, containers, file system) are not
# needed by cutl::xml::parser. configure would only fill cutl/details/config.h, which is written
# here with the same two definitions an external-Expat static build gets.
sed -e 's/#undef LIBCUTL_EXTERNAL_EXPAT/#define LIBCUTL_EXTERNAL_EXPAT 1/' \
    -e 's/#undef LIBCUTL_STATIC_LIB/#define LIBCUTL_STATIC_LIB 1/' \
    /work/source/cutl/details/config.h.in > /work/source/cutl/details/config.h
src="/work/source/cutl/exception.cxx /work/source/cutl/xml/parser.cxx /work/source/cutl/xml/qname.cxx /work/source/cutl/xml/value-traits.cxx"
inc='-I/work/source -I/work/expat/include'
common='-std=c++17 -O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $inc $src /work/harness.cpp /work/replay.cpp \
  /work/expat/lib/libexpat.a -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $inc $src /work/harness.cpp \
  /work/expat/lib/libexpat.a -o /work/fuzzer
