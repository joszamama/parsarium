#!/bin/sh
set -eu
src=/work/libgda-src
jobs=$(nproc)
options='--disable-shared --enable-static --without-ui --without-help --without-graphviz --disable-tools --disable-json --disable-crypto --without-libsoup --without-libsecret --without-gnome-keyring --disable-gdaui-gi --disable-vala --enable-introspection=no --enable-system-sqlite --disable-default-binary'
# clang 21 rejects libgda 5.2.10's GDestroyNotify casts by default; they are warnings in the release's era.
quiet='-Wno-incompatible-function-pointer-types -Wno-int-conversion -Wno-deprecated-declarations'
common='-std=gnu11 -O1 -g -fno-omit-frame-pointer'
glib_cflags=$(pkg-config --cflags glib-2.0 gobject-2.0 libxml-2.0)
glib_libs="$(pkg-config --libs gobject-2.0 gmodule-2.0 gthread-2.0 gio-2.0 libxml-2.0 sqlite3) -lm"

# Configures one tree, regenerates the Lemon parsers with the bundled lemon, removes their
# #line directives (so coverage maps to the generated C files), then builds libgda's core library.
build_tree() {
  tree=$1
  shift
  cp -a "$src" "$tree"
  (cd "$tree" && env "$@" ./configure $options > configure.log)
  make -C "$tree/libgda/sql-parser" lemon gen_def
  make -C "$tree/libgda/sql-parser" -i parser.c parser.h delimiter.c delimiter.h token_types.h
  sed -i '/^#line /d' "$tree/libgda/sql-parser/parser.c" "$tree/libgda/sql-parser/delimiter.c"
  make -C "$tree/libgda" -j"$jobs" typelibs_DATA= gir_DATA= INTROSPECTION_GIRS=
}

# Coverage build: the whole core library under LLVM source coverage; the replay prints the tree.
build_tree /work/build-cov CC=clang CFLAGS="-O1 -g $quiet -fprofile-instr-generate -fcoverage-mapping"
includes="-I/work/build-cov -I/work/build-cov/libgda $glib_cflags"
clang $common $includes -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/build-cov/libgda/.libs/libgda-5.0.a $glib_libs -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: only the Lemon grammar (parser.c) and the GdaSqlParser tokenizer and
  # driver (gda-sql-parser.c) are instrumented; the allowlist entry suffix-matches both.
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  build_tree /work/build-afl CC=clang CFLAGS="-O1 -g $quiet"
  for object in $(find /work/build-afl/libgda -name '*.o' | sort); do
    if nm "$object" | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "$(basename "$object")"; fi
  done | sort -u > /work/afl-instrumented-objects.txt
  printf '%s\n' gda-sql-parser.o parser.o > /work/afl-expected-objects.txt
  cmp /work/afl-instrumented-objects.txt /work/afl-expected-objects.txt
  clang $common -I/work/build-afl -I/work/build-afl/libgda $glib_cflags /work/parser-probe.c /work/build-afl/libgda/.libs/libgda-5.0.a $glib_libs -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang $common $includes -DPARSARIUM_FUZZER -fsanitize=fuzzer -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/build-cov/libgda/.libs/libgda-5.0.a $glib_libs -o /work/fuzzer
  clang $common $includes -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.c /work/build-cov/libgda/.libs/libgda-5.0.a $glib_libs -o /work/parser-probe
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
