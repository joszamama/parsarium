#!/bin/sh
set -eu
common='-std=c17 -O1 -g -fno-omit-frame-pointer -I/work/tomlc17-src/src -I/work'
src=/work/tomlc17-src/src/tomlc17.c
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c $src -lm -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: only the pinned src/tomlc17.c is instrumented.
  mkdir -p /work/afl-obj
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -c $src -o /work/afl-obj/tomlc17.o
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -c /work/parser-probe.c -o /work/afl-obj/parser-probe.o
  for object in /work/afl-obj/*.o; do
    if nm "$object" | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "$(basename "$object")"; fi
  done > /work/afl-instrumented-objects.txt
  test "$(cat /work/afl-instrumented-objects.txt)" = "tomlc17.o"
  clang /work/afl-obj/tomlc17.o /work/afl-obj/parser-probe.o -lm -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.c $src -lm -o /work/fuzzer
  clang $common -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.c $src -lm -o /work/parser-probe
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
