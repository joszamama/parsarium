#!/bin/sh
set -eu
common='-std=c++17 -O1 -g -fno-omit-frame-pointer'
sources='/work/source/src/lib_json/json_reader.cpp /work/source/src/lib_json/json_value.cpp /work/source/src/lib_json/json_writer.cpp'
includes='-I/work/source/include -I/work/source/src/lib_json'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $includes \
  $sources /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $includes \
  $sources /work/harness.cpp -o /work/fuzzer
