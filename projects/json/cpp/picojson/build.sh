#!/bin/sh
set -eu
# PICOJSON_USE_INT64 is the documented option that keeps JSON integers distinct from doubles.
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -DPICOJSON_USE_INT64 -I/work/source'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  clang++ $common /work/parser-probe.cpp -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang++ $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.cpp -o /work/fuzzer
  clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.cpp -o /work/parser-probe
fi
