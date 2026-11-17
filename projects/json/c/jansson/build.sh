#!/bin/sh
set -eu
cmake -S /work/jansson-src -B /work/jansson-config -DCMAKE_C_COMPILER=clang \
  -DJANSSON_BUILD_DOCS=OFF -DJANSSON_WITHOUT_TESTS=ON -DJANSSON_EXAMPLES=OFF > /dev/null
common='-std=c11 -O1 -g -fno-omit-frame-pointer -DHAVE_CONFIG_H'
includes='-I/work/jansson-config/include -I/work/jansson-config/private_include -I/work/jansson-src/src'
clang $common $includes -fprofile-instr-generate -fcoverage-mapping \
  /work/harness.c /work/replay.c /work/jansson-src/src/*.c -lm -o /work/replay
clang $common $includes -fsanitize=fuzzer,address,undefined \
  /work/harness.c /work/jansson-src/src/*.c -lm -o /work/fuzzer
