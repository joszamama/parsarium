#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 meson setup /work/build /work/source --prefix=/work/install --buildtype=plain -Ddefault_library=static \
 -Dpng=enabled -Dtests=disabled -Dfontconfig=disabled -Dfreetype=disabled -Dxlib=disabled -Dxcb=disabled \
 -Dglib=disabled -Dsymbol-lookup=disabled -Dzlib=disabled -Dtee=disabled -Dgtk_doc=false
meson compile -C /work/build -j 4
meson install -C /work/build
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig:/work/install/lib/aarch64-linux-gnu/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags cairo) /work/harness.cpp /work/replay.cpp $(pkg-config --static --libs cairo) -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags cairo) /work/harness.cpp $(pkg-config --static --libs cairo) -o /work/fuzzer
