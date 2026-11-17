#!/bin/sh
set -eu
# Only the cpprest JSON translation units and the UTF/locale helpers they call are
# compiled; /work/shim/stdafx.h replaces the precompiled header that pulls in HTTP,
# websocket and Boost.Asio headers. No cpprest source file is modified.
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -I/work/shim -I/work/source/Release/include'
json='/work/source/Release/src/json/json.cpp /work/source/Release/src/json/json_parsing.cpp /work/source/Release/src/json/json_serialization.cpp'
utils='/work/source/Release/src/utilities/asyncrt_utils.cpp'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $json $utils /work/harness.cpp -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  mkdir -p /work/obj
  for unit in $json $utils /work/parser-probe.cpp; do
    clang++ $common -c "$unit" -o "/work/obj/$(basename "$unit" .cpp).o"
  done
  # The allowlist must instrument exactly the three cpprest JSON objects.
  instrumented=$(for object in /work/obj/*.o; do
    if nm "$object" | grep -q '__afl_area_ptr'; then basename "$object"; fi
  done | tr '\n' ' ')
  test "$instrumented" = 'json.o json_parsing.o json_serialization.o '
  echo "$instrumented" > /work/instrumented-objects.txt
  clang++ /work/obj/*.o -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang++ $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined $json $utils /work/harness.cpp -o /work/fuzzer
  clang++ $common -fprofile-instr-generate -fcoverage-mapping $json $utils /work/parser-probe.cpp -o /work/parser-probe
fi
