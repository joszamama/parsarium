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
  rustflags='-C instrument-coverage'
  # Meson links the Rust staticlib into librsvg-2.so with the C driver, which needs
  # the profile runtime as well.
  rsvg_ldflags='-fprofile-instr-generate'
  ;;
afl)
  # librsvg's Rust crates get pcguard edges; the harness binary's AFL++ runtime
  # resolves the callbacks when it loads librsvg-2.so.
  rustflags='-C passes=sancov-module -C llvm-args=-sanitizer-coverage-level=3 -C llvm-args=-sanitizer-coverage-trace-pc-guard -C llvm-args=-sanitizer-coverage-prune-blocks=0 -C link-arg=-Wl,-z,undefs'
  rsvg_ldflags=''
  ;;
*)
  echo "unknown PARSARIUM_BUILD: $mode" >&2
  exit 2
  ;;
esac
# -Dtriplet makes cargo cross-style, so RUSTFLAGS reach librsvg's crates but not build
# scripts or proc macros. b_lundef=false lets the AFL++ build leave pcguard callbacks
# undefined in librsvg-2.so. GdkPixbuf integration is off: this path is the C API only.
CC=clang LDFLAGS="$rsvg_ldflags" RUSTFLAGS="$rustflags" \
 meson setup /work/rsvg-build /work/librsvg --prefix=/work/install --libdir=lib --buildtype=plain --wrap-mode=nodownload \
 -Ddefault_library=shared -Db_lundef=false -Dtriplet=aarch64-unknown-linux-gnu -Dpixbuf=disabled -Dpixbuf-loader=disabled \
 -Drsvg-convert=disabled -Dintrospection=disabled -Dvala=disabled -Ddocs=disabled -Davif=disabled -Dtests=false
RUSTFLAGS="$rustflags" meson compile -C /work/rsvg-build -j 4
RUSTFLAGS="$rustflags" meson install -C /work/rsvg-build
library=$(readlink -f /work/install/lib/librsvg-2.so)
case "$mode" in
coverage)
  readelf -SW "$library" | grep -q __llvm_covmap
  llvm-nm "$library" | grep -q ' __llvm_profile_write_file$'
  ;;
afl)
  readelf -SW "$library" | grep -q __sancov_guards
  llvm-nm -D --undefined-only "$library" | grep -q ' __sanitizer_cov_trace_pc_guard$'
  ;;
esac
cflags=$(pkg-config --cflags librsvg-2.0 cairo)
libs="$(pkg-config --libs librsvg-2.0 cairo) -lm"
if [ "$mode" = coverage ]; then
  clang $common -fprofile-instr-generate -fcoverage-mapping $cflags /work/harness.c /work/replay.c $libs -o /work/replay
  clang $common -fsanitize=fuzzer,address,undefined $cflags /work/harness.c $libs -o /work/fuzzer
else
  # Leave the harness itself uninstrumented, so every AFL++ edge comes from librsvg's Rust crates.
  printf 'fun: parsarium_uninstrumented_harness\n' > /work/afl-allowlist.txt
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  exported='-Wl,--export-dynamic-symbol=__sanitizer_cov_trace_pc_guard_init -Wl,--export-dynamic-symbol=__sanitizer_cov_trace_pc_guard'
  afl-clang-fast $common $cflags /work/harness.c /work/replay.c $libs $exported -o /work/replay
  afl-clang-fast $common -fsanitize=fuzzer,address,undefined -fno-sanitize=function $cflags /work/harness.c $libs $exported -o /work/fuzzer
  for binary in /work/replay /work/fuzzer; do
    nm -D --defined-only "$binary" | grep -q ' __sanitizer_cov_trace_pc_guard_init$'
  done
fi
