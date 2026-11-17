#!/bin/sh
set -eu
# RYML_DEFAULT_CALLBACK_USES_EXCEPTIONS makes the documented default error
# callbacks throw instead of aborting, so the harness can reject bad input.
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -DRYML_DEFAULT_CALLBACK_USES_EXCEPTIONS'
sources=$(ls /work/source/src/c4/yml/*.cpp /work/source/ext/c4core.src/c4/*.cpp)
includes='-I/work/source/src -I/work/source/ext/c4core.src'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $includes \
  $sources /work/harness.cpp /work/replay.cpp -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # AFL++ overlay: no ASan, whose allocator made a few edges vary between
  # identical replays of a valid control.
  clang++ $common -fsanitize=fuzzer $includes $sources /work/harness.cpp -o /work/fuzzer
else
  clang++ $common -fsanitize=fuzzer,address,undefined $includes \
    $sources /work/harness.cpp -o /work/fuzzer
fi
