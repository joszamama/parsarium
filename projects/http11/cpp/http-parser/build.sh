#!/bin/sh
set -eu
src=/work/http-parser-2.9.4
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
  -c "$src/http_parser.c" -o /work/parser-coverage.o
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
  /work/harness.cpp /work/replay.cpp /work/parser-coverage.o -o /work/replay
clang $common -fsanitize=fuzzer-no-link,address,undefined -I"$src" \
  -c "$src/http_parser.c" -o /work/parser-fuzz.o
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -I"$src" \
  /work/harness.cpp /work/parser-fuzz.o -o /work/fuzzer
