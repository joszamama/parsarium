#!/bin/sh
set -eu
mode=${PARSARIUM_BUILD:-coverage}
export CARGO_NET_OFFLINE=true
export LLVM_PROFILE_FILE=/tmp/parsarium-build-%m.profraw
rustc --version --verbose | grep -q '^LLVM version: 21\.'
case "$mode" in
coverage)
  export RUSTFLAGS='-C instrument-coverage'
  export CARGO_TARGET_DIR=/work/target/coverage
  ;;
afl)
  # Instrument only the usvg crate. The render engine and C adapter contribute
  # no guards, so AFL's map is parser-scoped rather than renderer feedback.
  export RUSTFLAGS='-C link-arg=-Wl,-z,undefs'
  export RUSTC_WRAPPER=/work/rustc-usvg-wrapper.sh
  export CARGO_TARGET_DIR=/work/target/afl
  ;;
*) echo "unknown PARSARIUM_BUILD: $mode" >&2; exit 2 ;;
esac
cd /work/source
cargo build --release --locked -p resvg-capi -j 4
cp "$CARGO_TARGET_DIR/release/libresvg.so" /work/libresvg.so
if [ "$mode" = coverage ]; then
  readelf -SW /work/libresvg.so | grep -q __llvm_covmap
  llvm-nm /work/libresvg.so | grep -q ' __llvm_profile_write_file$'
  clang -O1 -g -fprofile-instr-generate -fcoverage-mapping -I/work/source/crates/c-api \
    /work/harness.c /work/replay.c -L/work -Wl,-rpath,/work -lresvg -lm -o /work/replay
  clang -O1 -g -fsanitize=fuzzer,address,undefined -I/work/source/crates/c-api \
    /work/harness.c -L/work -Wl,-rpath,/work -lresvg -lm -o /work/fuzzer
else
  readelf -SW /work/libresvg.so | grep -q __sancov_guards
  printf 'fun: parsarium_uninstrumented_harness\n' > /work/afl-allowlist.txt
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  exported='-Wl,--export-dynamic-symbol=__sanitizer_cov_trace_pc_guard_init -Wl,--export-dynamic-symbol=__sanitizer_cov_trace_pc_guard'
  afl-clang-fast -O1 -g -I/work/source/crates/c-api \
    /work/harness.c /work/replay.c -L/work -Wl,-rpath,/work -lresvg -lm $exported -o /work/replay
  afl-clang-fast -O1 -g -fsanitize=fuzzer,address,undefined -fno-sanitize=function \
    -I/work/source/crates/c-api /work/harness.c -L/work -Wl,-rpath,/work -lresvg -lm $exported -o /work/fuzzer
  nm -D --defined-only /work/replay | grep -q ' __sanitizer_cov_trace_pc_guard_init$'
fi
