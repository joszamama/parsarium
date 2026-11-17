#!/bin/sh
set -eu
src=/work/libpg_query-src
jobs=$(nproc)
# Coverage build: the whole library under LLVM source coverage; the replay prints the parse tree.
cp -a "$src" /work/build-cov
make -C /work/build-cov -j"$jobs" CC=clang CFLAGS='-fprofile-instr-generate -fcoverage-mapping' build
common='-std=gnu11 -O1 -g -fno-omit-frame-pointer'
clang $common -I/work/build-cov -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/build-cov/libpg_query.a -lpthread -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: only the PostgreSQL grammar, scanner and raw_parser entry are instrumented.
  cp -a "$src" /work/build-afl
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt make -C /work/build-afl -j"$jobs" CC=clang build
  for object in /work/build-afl/src/*.o /work/build-afl/src/postgres/*.o /work/build-afl/vendor/xxhash/*.o; do
    if nm "$object" | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "$(basename "$object")"; fi
  done | sort > /work/afl-instrumented-objects.txt
  printf '%s\n' src_backend_parser_gram.o src_backend_parser_parser.o src_backend_parser_scan.o > /work/afl-expected-objects.txt
  cmp /work/afl-instrumented-objects.txt /work/afl-expected-objects.txt
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -I/work/build-afl /work/parser-probe.c /work/build-afl/libpg_query.a -lpthread -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang $common -I/work/build-cov -DPARSARIUM_FUZZER -fsanitize=fuzzer -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/build-cov/libpg_query.a -lpthread -o /work/fuzzer
  clang $common -I/work/build-cov -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.c /work/build-cov/libpg_query.a -lpthread -o /work/parser-probe
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
