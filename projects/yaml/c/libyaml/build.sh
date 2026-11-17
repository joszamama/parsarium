#!/bin/sh
set -eu
common='-std=gnu11 -O1 -g -fno-omit-frame-pointer -DYAML_DECLARE_STATIC -DYAML_VERSION_MAJOR=0 -DYAML_VERSION_MINOR=2 -DYAML_VERSION_PATCH=5 -DYAML_VERSION_STRING="0.2.5" -I/work/libyaml-src/include -I/work'
names='api reader scanner parser loader'
srcs=''
for name in $names; do srcs="$srcs /work/libyaml-src/src/$name.c"; done
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c $srcs -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: only the five pinned libyaml loader sources are instrumented.
  mkdir -p /work/afl-obj
  for name in $names; do
    AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -c /work/libyaml-src/src/$name.c -o /work/afl-obj/$name.o
  done
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -c /work/parser-probe.c -o /work/afl-obj/parser-probe.o
  for object in /work/afl-obj/*.o; do
    if nm "$object" | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "$(basename "$object")"; fi
  done > /work/afl-instrumented-objects.txt
  test "$(tr '\n' ' ' < /work/afl-instrumented-objects.txt)" = "api.o loader.o parser.o reader.o scanner.o "
  clang /work/afl-obj/*.o -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.c $srcs -o /work/fuzzer
  clang $common -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.c $srcs -o /work/parser-probe
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
