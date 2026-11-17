#!/bin/sh
set -eu
cov='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
afl=0
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # AFL++ instruments only GMarkup (glib/gmarkup.c) and libxmlb's src/xb-*.c.
  afl=1
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
fi
# GLib from the pinned release, static and out of tree: GMarkup is the XML
# tokenizer libxmlb's builder calls; system GLib would be uninstrumented.
CC=clang CFLAGS="$cov" LDFLAGS='-fprofile-instr-generate' \
 meson setup /work/glib-build /work/glib --prefix=/work/prefix --libdir=lib --buildtype=plain \
  -Ddefault_library=static -Dtests=false -Dinstalled_tests=false -Dintrospection=disabled -Dnls=disabled \
  -Dselinux=disabled -Dxattr=false -Dlibmount=disabled -Dman-pages=disabled -Ddocumentation=false \
  -Dsysprof=disabled -Dlibelf=disabled -Ddtrace=disabled -Dsystemtap=disabled --wrap-mode=nofallback
ninja -C /work/glib-build install
export PKG_CONFIG_PATH=/work/prefix/lib/pkgconfig
CC=clang CFLAGS="$cov" LDFLAGS='-fprofile-instr-generate' \
 meson setup /work/xmlb-build /work/source --prefix=/work/prefix --libdir=lib --buildtype=plain \
  -Ddefault_library=static -Dintrospection=false -Dgtkdoc=false -Dtests=false -Dcli=false \
  -Dlzma=disabled -Dzstd=disabled --wrap-mode=nofallback
ninja -C /work/xmlb-build install
if [ "$afl" = 1 ]; then
  # Members that carry AFL++ instrumentation must be exactly gmarkup.c and libxmlb sources.
  nm -A /work/prefix/lib/libglib-2.0.a /work/prefix/lib/libgobject-2.0.a /work/prefix/lib/libgio-2.0.a \
     /work/prefix/lib/libgmodule-2.0.a /work/prefix/lib/libxmlb.a 2>/dev/null \
   | grep '__sanitizer_cov_trace_pc_guard_init' | sed 's/^[^:]*://; s/:.*//' | sort -u > /work/afl-instrumented-objects.txt
  cat /work/afl-instrumented-objects.txt
  grep -qx 'gmarkup.c.o' /work/afl-instrumented-objects.txt
  grep -q '^xb-builder.c.o$' /work/afl-instrumented-objects.txt
  if grep -v -e '^gmarkup.c.o$' -e '^xb-[a-z-]*\.c\.o$' /work/afl-instrumented-objects.txt; then
    echo 'unexpected AFL++-instrumented object' >&2; exit 1
  fi
fi
common='-O1 -g -fno-omit-frame-pointer'
flags=$(pkg-config --static --cflags --libs xmlb)
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c $flags -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -fprofile-instr-generate /work/harness.c $flags -o /work/fuzzer
