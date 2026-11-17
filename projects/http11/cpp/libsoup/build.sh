#!/bin/sh
set -eu

# One libsoup build carries LLVM source coverage for replay and sanitizer
# coverage for the fuzzer, so both binaries exercise instrumented libsoup code.
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
CC=clang CFLAGS="$common" LDFLAGS="$common" \
  meson setup /work/libsoup-build /work/source --buildtype=plain \
  --default-library=static --wrap-mode=nofallback -Dauto_features=disabled \
  -Dtls_check=false -Dtests=false -Dinstalled_tests=false -Ddoc_tests=false
ninja -C /work/libsoup-build libsoup/libsoup-3.0.a

soup='/work/libsoup-build/libsoup/libsoup-3.0.a'
glib_cflags=$(pkg-config --cflags gio-2.0)
deps=$(pkg-config --libs gio-2.0 gobject-2.0 gmodule-2.0 glib-2.0 libnghttp2 libpsl sqlite3 zlib)
# Uninstalled header tree: the same include directories libsoup/meson.build uses.
soup_includes='-I/work/source -I/work/libsoup-build/libsoup'
for dir in . auth cookies content-decoder hsts http1 http2 server server/http1 server/http2 websocket; do
  soup_includes="$soup_includes -I/work/source/libsoup/$dir"
done

clang++ -std=c++17 $common $glib_cflags $soup_includes \
  -c /work/harness.cpp -o /work/harness.o
clang++ -std=c++17 $common -c /work/replay.cpp -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o "$soup" $deps -o /work/replay

clang++ -std=c++17 $common $glib_cflags -c /work/fuzz.cpp -o /work/fuzz.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o "$soup" $deps -o /work/fuzzer
