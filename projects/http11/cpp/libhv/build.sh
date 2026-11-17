#!/bin/sh
set -eu
src=/work/libhv-1.3.1
common='-O1 -g -fno-omit-frame-pointer'
include="-I$src -I$src/http"
for file in http_parser httpdef; do
  clang $common -fprofile-instr-generate -fcoverage-mapping $include \
    -c "$src/http/$file.c" -o /work/$file-coverage.o
  clang $common -fsanitize=fuzzer-no-link,address,undefined $include \
    -c "$src/http/$file.c" -o /work/$file-fuzz.o
done
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping $include \
  /work/harness.cpp /work/replay.cpp /work/http_parser-coverage.o /work/httpdef-coverage.o -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined $include \
  /work/harness.cpp /work/http_parser-fuzz.o /work/httpdef-fuzz.o -o /work/fuzzer
