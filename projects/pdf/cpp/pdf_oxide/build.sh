#!/bin/sh
set -eu
mode=${PARSARIUM_BUILD:-coverage}
export CARGO_NET_OFFLINE=true
export LLVM_PROFILE_FILE=/tmp/parsarium-build-%m.profraw
# Upstream [profile.release] sets lto = true and strip = true. Fat LTO would
# re-optimize every dependency under pdf_oxide's flags (spreading the sancov
# pass beyond the crate) and stripping hides the symbols checked below.
export CARGO_PROFILE_RELEASE_LTO=false
export CARGO_PROFILE_RELEASE_STRIP=false
rustc --version --verbose | grep -q '^LLVM version: 21\.'
case "$mode" in
coverage)
  export RUSTFLAGS='-C instrument-coverage'
  export CARGO_TARGET_DIR=/work/target/coverage
  ;;
afl)
  # Instrument only the pdf_oxide crate. Its dependencies (flate2/zlib-rs, nom,
  # regex, ...) and the C++ harness contribute no guards.
  export RUSTFLAGS='-C link-arg=-Wl,-z,undefs'
  export RUSTC_WRAPPER=/work/rustc-pdf-oxide-wrapper.sh
  export CARGO_TARGET_DIR=/work/target/afl
  ;;
*) echo "unknown PARSARIUM_BUILD: $mode" >&2; exit 2 ;;
esac
cd /work/source
cargo build --release --locked -p pdf_oxide --lib -j 4
cp "$CARGO_TARGET_DIR/release/libpdf_oxide.so" /work/libpdf_oxide.so
cxxflags='-std=c++17 -O1 -g -Wall -Wextra -Werror -I/work/source/cpp/include -I/work/source/include'
if [ "$mode" = coverage ]; then
  readelf -SW /work/libpdf_oxide.so | grep -q __llvm_covmap
  llvm-nm /work/libpdf_oxide.so | grep -q ' __llvm_profile_write_file$'
  clang++ $cxxflags -fprofile-instr-generate -fcoverage-mapping \
    /work/harness.cpp /work/replay.cpp -L/work -Wl,-rpath,/work -lpdf_oxide -o /work/replay
  clang++ $cxxflags -fsanitize=fuzzer,address,undefined \
    /work/harness.cpp /work/fuzz.cpp -L/work -Wl,-rpath,/work -lpdf_oxide -o /work/fuzzer
else
  readelf -SW /work/libpdf_oxide.so | grep -q __sancov_guards
  printf 'fun: parsarium_uninstrumented_harness\n' > /work/afl-allowlist.txt
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  exported='-Wl,--export-dynamic-symbol=__sanitizer_cov_trace_pc_guard_init -Wl,--export-dynamic-symbol=__sanitizer_cov_trace_pc_guard'
  afl-clang-fast++ $cxxflags \
    /work/harness.cpp /work/replay.cpp -L/work -Wl,-rpath,/work -lpdf_oxide $exported -o /work/replay
  afl-clang-fast++ $cxxflags -fsanitize=fuzzer,address,undefined -fno-sanitize=function \
    /work/harness.cpp /work/fuzz.cpp -L/work -Wl,-rpath,/work -lpdf_oxide $exported -o /work/fuzzer
  nm -D --defined-only /work/replay | grep -q ' __sanitizer_cov_trace_pc_guard_init$'
fi
