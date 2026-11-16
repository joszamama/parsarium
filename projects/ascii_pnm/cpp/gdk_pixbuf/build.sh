#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 meson setup /work/build /work/source --prefix=/work/install --buildtype=plain -Ddefault_library=static \
 -Dpng=enabled -Dothers=enabled -Dbuiltin_loaders=all -Dtiff=disabled -Djpeg=disabled -Dgif=disabled -Dglycin=disabled \
 -Dintrospection=disabled -Ddocumentation=false -Dman=false -Dtests=false -Dinstalled_tests=false -Dthumbnailer=disabled -Dgio_sniffing=false
meson compile -C /work/build -j 4
meson install -C /work/build
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig:/work/install/lib/aarch64-linux-gnu/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags gdk-pixbuf-2.0) /work/harness.cpp /work/replay.cpp $(pkg-config --static --libs gdk-pixbuf-2.0) -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags gdk-pixbuf-2.0) /work/harness.cpp $(pkg-config --static --libs gdk-pixbuf-2.0) -o /work/fuzzer
