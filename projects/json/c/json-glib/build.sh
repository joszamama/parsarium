#!/bin/sh
set -eu
# Build the pinned JSON-GLib as a static library once per instrumentation, then
# link the harness against it and the system GLib/GObject/GIO shared libraries.
common='-O1 -g -fno-omit-frame-pointer'
build_json_glib() {
  rm -rf "$1"
  CC=clang meson setup "$1" /work/json-glib-src --default-library=static --buildtype=plain \
    -Dc_args="$2" -Dintrospection=disabled -Ddocumentation=disabled -Dman=false \
    -Dtests=false -Dconformance=false -Dinstalled_tests=false -Dnls=disabled > "$1.log"
  ninja -C "$1" json-glib/libjson-glib-1.0.a >> "$1.log"
}
deps=$(pkg-config --cflags --libs gio-2.0 gobject-2.0 glib-2.0)
build_json_glib /work/build-cov "$common -fprofile-instr-generate -fcoverage-mapping"
include='-I/work/json-glib-src -I/work/build-cov -I/work/build-cov/json-glib -I/work'
clang $common $include -fprofile-instr-generate -fcoverage-mapping /work/harness.c \
  /work/build-cov/json-glib/libjson-glib-1.0.a $deps -lm -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: JsonParser, JsonScanner and the node/object/array/value tree only.
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  build_json_glib /work/build-afl "$common"
  clang $common $include -c /work/parser-probe.c $(pkg-config --cflags gio-2.0) -o /work/parser-probe.o
  for object in /work/build-afl/json-glib/libjson-glib-1.0.a.p/*.o /work/parser-probe.o; do
    if nm "$object" | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "$(basename "$object")"; fi
  done > /work/afl-instrumented-objects.txt
  test "$(tr '\n' ' ' < /work/afl-instrumented-objects.txt)" = "json-array.c.o json-node.c.o json-object.c.o json-parser.c.o json-scanner.c.o json-value.c.o "
  clang /work/parser-probe.o /work/build-afl/json-glib/libjson-glib-1.0.a $deps -lm -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang $common $include -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.c \
    /work/build-cov/json-glib/libjson-glib-1.0.a $deps -lm -o /work/parser-probe
  build_json_glib /work/build-fuzz "$common -fsanitize=fuzzer-no-link,address,undefined"
  clang $common $include -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.c \
    /work/build-fuzz/json-glib/libjson-glib-1.0.a $deps -lm -o /work/fuzzer
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
