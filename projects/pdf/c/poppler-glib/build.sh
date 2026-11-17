#!/bin/sh
set -eu
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common="-O1 -g -fno-omit-frame-pointer $(pkg-config --cflags poppler-glib) -L/work/install/lib -lpoppler-glib $(pkg-config --libs gobject-2.0 glib-2.0) -Wl,-rpath,/work/install/lib -Wl,-export-dynamic"
clang -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c $common -o /work/replay
clang -fsanitize=fuzzer,address,undefined /work/harness.c $common -o /work/fuzzer
