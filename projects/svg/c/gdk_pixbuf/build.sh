#!/bin/sh
set -eu
# PARSARIUM_BUILD=coverage builds the replay/libFuzzer image; afl builds the AFL++ overlay.
mode=${PARSARIUM_BUILD:-coverage}
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
export CARGO_NET_OFFLINE=true
export LLVM_PROFILE_FILE=/tmp/parsarium-build-%m.profraw
rustc --version --verbose | grep -q '^LLVM version: 21\.'
common='-O1 -g -fno-omit-frame-pointer'
case "$mode" in
coverage)
  pixbuf_cflags="$common -fprofile-instr-generate -fcoverage-mapping"
  pixbuf_ldflags='-fprofile-instr-generate'
  rustflags='-C instrument-coverage'
  rsvg_ldflags='-fprofile-instr-generate'
  install_preload=''
  ;;
afl)
  # librsvg gets pcguard edges resolved by the AFL++ runtime in the harness;
  # the stub only lets gdk-pixbuf-query-loaders open the loader at install time.
  pixbuf_cflags="$common"
  pixbuf_ldflags=''
  rustflags='-C passes=sancov-module -C llvm-args=-sanitizer-coverage-level=3 -C llvm-args=-sanitizer-coverage-trace-pc-guard -C llvm-args=-sanitizer-coverage-prune-blocks=0 -C link-arg=-Wl,-z,undefs'
  rsvg_ldflags=''
  printf '%s\n' 'void __sanitizer_cov_trace_pc_guard_init(unsigned *start, unsigned *stop) { (void)start; (void)stop; }' \
    'void __sanitizer_cov_trace_pc_guard(unsigned *guard) { (void)guard; }' > /work/sancov-stub.c
  clang -shared -fPIC /work/sancov-stub.c -o /work/sancov-stub.so
  install_preload=/work/sancov-stub.so
  ;;
*)
  echo "unknown PARSARIUM_BUILD: $mode" >&2
  exit 2
  ;;
esac
CC=clang CFLAGS="$pixbuf_cflags" LDFLAGS="$pixbuf_ldflags" \
 meson setup /work/build /work/source --prefix=/work/install --libdir=lib --buildtype=plain --wrap-mode=nodownload \
 -Ddefault_library=shared -Dpng=disabled -Djpeg=disabled -Dtiff=disabled -Dgif=disabled -Dothers=disabled \
 -Dglycin=disabled -Dbuiltin_loaders=none -Dintrospection=disabled -Ddocumentation=false -Dman=false \
 -Dtests=false -Dinstalled_tests=false -Dthumbnailer=disabled -Dgio_sniffing=false
meson compile -C /work/build -j 4
meson install -C /work/build
# librsvg's Rust staticlib is linked into librsvg-2.so by meson; b_lundef=false lets the
# AFL++ build leave pcguard callbacks for the harness to provide.
CC=clang LDFLAGS="$rsvg_ldflags" RUSTFLAGS="$rustflags" \
 meson setup /work/rsvg-build /work/librsvg --prefix=/work/install --libdir=lib --buildtype=plain --wrap-mode=nodownload \
 -Ddefault_library=shared -Db_lundef=false -Dtriplet=aarch64-unknown-linux-gnu -Dpixbuf=enabled -Dpixbuf-loader=enabled \
 -Drsvg-convert=disabled -Dintrospection=disabled -Dvala=disabled -Ddocs=disabled -Davif=disabled -Dtests=false
RUSTFLAGS="$rustflags" meson compile -C /work/rsvg-build -j 4
RUSTFLAGS="$rustflags" LD_PRELOAD="$install_preload" meson install -C /work/rsvg-build
loader=/work/install/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader_svg.so
test -f "$loader"
grep -q '"svg"' /work/install/lib/gdk-pixbuf-2.0/2.10.0/loaders.cache
case "$mode" in
coverage) section=__llvm_covmap ;;
afl) section=__sancov_guards ;;
esac
for object in "$(readlink -f /work/install/lib/librsvg-2.so)" "$loader"; do
  readelf -SW "$object" | grep -q "$section"
done
if [ "$mode" = coverage ]; then
  llvm-nm /work/install/lib/librsvg-2.so | grep -q ' __llvm_profile_write_file$'
fi
cflags=$(pkg-config --cflags gdk-pixbuf-2.0)
libs=$(pkg-config --libs gdk-pixbuf-2.0)
if [ "$mode" = coverage ]; then
  clang $common -fprofile-instr-generate -fcoverage-mapping $cflags /work/harness.c /work/replay.c $libs -o /work/replay
  clang $common -fsanitize=fuzzer,address,undefined $cflags /work/harness.c $libs -o /work/fuzzer
else
  # Leave the harness itself uninstrumented, so every AFL++ edge comes from librsvg's Rust stack.
  printf 'fun: parsarium_uninstrumented_harness\n' > /work/afl-allowlist.txt
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  exported='-Wl,--export-dynamic-symbol=__sanitizer_cov_trace_pc_guard_init -Wl,--export-dynamic-symbol=__sanitizer_cov_trace_pc_guard'
  afl-clang-fast $common $cflags /work/harness.c /work/replay.c $libs $exported -o /work/replay
  afl-clang-fast $common -fsanitize=fuzzer,address,undefined -fno-sanitize=function $cflags /work/harness.c $libs $exported -o /work/fuzzer
  for binary in /work/replay /work/fuzzer; do
    nm -D --defined-only "$binary" | grep -q ' __sanitizer_cov_trace_pc_guard_init$'
  done
fi
