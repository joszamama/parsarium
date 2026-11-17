#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
CC=clang CFLAGS="$common" LDFLAGS='-fprofile-instr-generate' \
  meson setup /work/build /work/source --prefix=/work/install --libdir=lib \
  --buildtype=plain \
  -Dx11-backend=true -Dwayland-backend=false -Dbroadway-backend=false \
  -Dmedia-gstreamer=disabled -Dprint-cups=disabled -Dvulkan=disabled \
  -Df16c=disabled -Dintrospection=disabled -Ddocumentation=false \
  -Dbuild-demos=false -Dbuild-testsuite=false -Dbuild-examples=false -Dbuild-tests=false
meson compile -C /work/build gtk-4 -j 3

gtk_lib=$(find /work/build/gtk -maxdepth 1 -name 'libgtk-4.so.1.*' -type f -print -quit)
test -n "$gtk_lib"
gtk_cflags=$(pkg-config --cflags gtk4)
glib_libs=$(pkg-config --libs gobject-2.0 glib-2.0)
clang -std=c11 $common $gtk_cflags -c /work/harness.c -o /work/harness.o
clang -std=c11 $common $gtk_cflags -c /work/replay.c -o /work/replay.o
clang $common /work/harness.o /work/replay.o "$gtk_lib" $glib_libs \
  -Wl,-rpath,/work/lib -o /work/replay-bin

clang -std=c11 -O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer-no-link,address,undefined \
  $gtk_cflags -c /work/harness.c -o /work/harness-fuzz.o
clang -O1 -g -fno-omit-frame-pointer -fprofile-instr-generate \
  -fsanitize=fuzzer,address,undefined /work/harness-fuzz.o "$gtk_lib" $glib_libs \
  -Wl,-rpath,/work/lib -o /work/fuzzer-bin
