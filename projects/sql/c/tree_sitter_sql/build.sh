#!/bin/sh
set -eu
common='-std=gnu11 -O1 -g -fno-omit-frame-pointer'
include='-I/work/src/tree-sitter/lib/include -I/work/src/tree-sitter/lib/src -I/work/src/tree-sitter-sql/src'
# Compiles the tree-sitter runtime (lib.c amalgamation) and the SQL grammar (generated parser.c and
# the external scanner) into one object directory; extra flags follow the directory argument.
objects() {
  out=$1
  shift
  mkdir -p "$out"
  clang $common "$@" $include -c /work/src/tree-sitter/lib/src/lib.c -o "$out/lib.o"
  clang $common "$@" $include -c /work/src/tree-sitter-sql/src/parser.c -o "$out/sql_parser.o"
  clang $common "$@" $include -c /work/src/tree-sitter-sql/src/scanner.c -o "$out/sql_scanner.o"
}
coverage='-fprofile-instr-generate -fcoverage-mapping'
# Coverage build: runtime and grammar under LLVM source coverage; the replay prints the syntax tree.
objects /work/build-cov $coverage
clang $common $coverage $include /work/harness.c /work/build-cov/lib.o /work/build-cov/sql_parser.o /work/build-cov/sql_scanner.o -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: only the tree-sitter runtime and the SQL grammar sources are instrumented.
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  objects /work/build-afl
  clang $common $include -c /work/parser-probe.c -o /work/build-afl/probe.o
  for object in /work/build-afl/*.o; do
    if nm "$object" | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "$(basename "$object")"; fi
  done | sort > /work/afl-instrumented-objects.txt
  printf '%s\n' lib.o sql_parser.o sql_scanner.o > /work/afl-expected-objects.txt
  cmp /work/afl-instrumented-objects.txt /work/afl-expected-objects.txt
  clang $common /work/build-afl/probe.o /work/build-afl/lib.o /work/build-afl/sql_parser.o /work/build-afl/sql_scanner.o -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang $common $coverage $include -DPARSARIUM_FUZZER -fsanitize=fuzzer /work/harness.c /work/build-cov/lib.o /work/build-cov/sql_parser.o /work/build-cov/sql_scanner.o -o /work/fuzzer
  clang $common $coverage $include /work/parser-probe.c /work/build-cov/lib.o /work/build-cov/sql_parser.o /work/build-cov/sql_scanner.o -o /work/parser-probe
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
