#!/bin/sh
set -eu
common='-std=c11 -O1 -g -fno-omit-frame-pointer -I/work/jsonh-src -I/work'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map. json.h is header-only, so the allowlist selects
  # functions by their json.h debug location. A PARSARIUM_NO_PARSE build of the
  # same probe must map no edges, which shows main() is not instrumented.
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common /work/parser-probe.c -o /work/parser-probe
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -DPARSARIUM_NO_PARSE /work/parser-probe.c -o /work/parser-probe-no-parse
  nm /work/parser-probe | grep -q ' json_parse_ex$'
  echo 'parser-probe.c: json.h functions only (allowlist by debug location)' > /work/afl-instrumented-objects.txt
  cp /work/parser-probe /work/fuzzer
else
  clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.c -o /work/fuzzer
  clang $common -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.c -o /work/parser-probe
  clang $common -DPARSARIUM_NO_PARSE /work/parser-probe.c -o /work/parser-probe-no-parse
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
