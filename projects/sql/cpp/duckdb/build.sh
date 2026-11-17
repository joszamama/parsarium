#!/bin/sh
set -eu
src=/work/duckdb-src
jobs=$(nproc)
# Core library only: no shell, unit tests, unity sources or optional extensions. The release tarball
# has no .git, so the version string is given explicitly (v2.0.0 tag commit d54cbbe3df17).
options='-G Ninja -DCMAKE_BUILD_TYPE=Release -DBUILD_SHELL=0 -DBUILD_UNITTESTS=0 -DDISABLE_UNITY=1 -DENABLE_SANITIZER=0 -DENABLE_UBSAN=0 -DSKIP_EXTENSIONS=parquet;json;icu;jemalloc -DOVERRIDE_GIT_DESCRIBE=v2.0.0-0-gd54cbbe3df'
# DuckDB builds without RTTI; the harness must match.
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -fno-rtti'

build_tree() {
  tree=$1
  flags=$2
  cp -a "$src" "$tree"
  cmake -S "$tree" -B "$tree/build" $options -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_C_FLAGS="$flags" -DCMAKE_CXX_FLAGS="$flags" > "$tree/cmake.log"
  cmake --build "$tree/build" --target duckdb_static -j"$jobs" > "$tree/build.log"
}

link_libs() {
  echo "-Wl,--start-group $(find "$1/build" -name '*.a' | sort | tr '\n' ' ') -Wl,--end-group -lpthread -ldl -lm"
}

if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: only DuckDB's parser sources (PEG tokenizer, matcher and transformer,
  # parsed expression, statement and table-reference constructors under src/parser) are instrumented.
  # The overlay uses the AFL++ tree for its replay; it has no coverage tree of its own.
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  build_tree /work/build-afl ''
  for object in $(find /work/build-afl/build -name '*.o' | sort); do
    if nm "$object" 2>/dev/null | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "${object#/work/build-afl/build/}"; fi
  done > /work/afl-instrumented-objects.txt
  test -s /work/afl-instrumented-objects.txt
  if grep -v '^src/parser/' /work/afl-instrumented-objects.txt; then echo 'unexpected AFL++ objects' >&2; exit 1; fi
  libs=$(link_libs /work/build-afl)
  clang++ $common -I/work/build-afl/src/include /work/parser-probe.cpp $libs -o /work/parser-probe
  clang++ $common -I/work/build-afl/src/include /work/harness.cpp $libs -o /work/replay
  cp /work/parser-probe /work/fuzzer
  mkdir -p /work/build-cov/src/parser
else
  # Coverage build: the core library under LLVM source coverage; the replay prints the summary.
  build_tree /work/build-cov '-fprofile-instr-generate -fcoverage-mapping'
  libs=$(link_libs /work/build-cov)
  cov='-fprofile-instr-generate -fcoverage-mapping'
  clang++ $common $cov -I/work/build-cov/src/include /work/harness.cpp $libs -o /work/replay
  clang++ $common $cov -DPARSARIUM_FUZZER -fsanitize=fuzzer -I/work/build-cov/src/include /work/harness.cpp $libs -o /work/fuzzer
  clang++ $common $cov -I/work/build-cov/src/include /work/parser-probe.cpp $libs -o /work/parser-probe
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
