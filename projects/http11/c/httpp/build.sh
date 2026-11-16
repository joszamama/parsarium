#!/bin/sh
set -eu
src=/work/httpp-2.0.0
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping -I"$src" \
  /work/harness.c /work/replay.c -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -I"$src" \
  /work/harness.c -o /work/fuzzer
