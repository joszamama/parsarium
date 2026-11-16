#!/bin/sh
set -eu
options='--auto-features=disabled -Ddocs=false -Dintrospection=false -Dvapigen=disabled -Dgtk-doc=false -Dgi-docgen=disabled -Doperation-test=false'
CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  meson setup /work/build-cov /work/source --prefix=/opt/gegl-cov --libdir=lib --buildtype=debug $options
meson compile -C /work/build-cov -j4
meson install -C /work/build-cov --no-rebuild
CC=clang CFLAGS='-O1 -g' \
  meson setup /work/build-fuzz /work/source --prefix=/opt/gegl-fuzz --libdir=lib --buildtype=debug -Db_sanitize=address,undefined -Db_lundef=false $options
meson compile -C /work/build-fuzz -j4
meson install -C /work/build-fuzz --no-rebuild
PKG_CONFIG_PATH=/opt/gegl-cov/lib/pkgconfig pkg-config --exists gegl-0.4
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  $(PKG_CONFIG_PATH=/opt/gegl-cov/lib/pkgconfig pkg-config --cflags gegl-0.4) \
  /work/harness.c /work/replay.c \
  $(PKG_CONFIG_PATH=/opt/gegl-cov/lib/pkgconfig pkg-config --libs gegl-0.4) \
  -Wl,-rpath,/opt/gegl-cov/lib -o /work/replay
clang -O1 -g -fsanitize=fuzzer,address,undefined \
  $(PKG_CONFIG_PATH=/opt/gegl-fuzz/lib/pkgconfig pkg-config --cflags gegl-0.4) \
  /work/harness.c \
  $(PKG_CONFIG_PATH=/opt/gegl-fuzz/lib/pkgconfig pkg-config --libs gegl-0.4) \
  -Wl,-rpath,/opt/gegl-fuzz/lib -o /work/fuzzer
