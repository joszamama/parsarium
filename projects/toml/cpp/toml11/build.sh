#!/bin/sh
set -eu
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -I/work/source/include'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  clang++ $common /work/parser-probe.cpp -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang++ $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.cpp -o /work/fuzzer
  clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.cpp -o /work/parser-probe
fi
