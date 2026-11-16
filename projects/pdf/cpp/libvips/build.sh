#!/bin/sh
set -eu
CC=clang CXX=clang++ CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 meson setup /work/build /work/source --prefix=/work/install --buildtype=plain -Ddefault_library=static \
 -Dmodules=disabled -Dcplusplus=true -Dexamples=false -Ddocs=false -Dintrospection=disabled \
 -Dpng=enabled -Drsvg=enabled -Dpoppler=enabled -Dpdfium=disabled
meson compile -C /work/build -j 4
meson install -C /work/build
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig:/work/install/lib/aarch64-linux-gnu/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags vips-cpp) /work/harness.cpp /work/replay.cpp $(pkg-config --libs vips-cpp) -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags vips-cpp) /work/harness.cpp $(pkg-config --libs vips-cpp) -o /work/fuzzer
