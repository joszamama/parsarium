#!/bin/sh
set -eu
cmake -S /work/json-c-src -B /work/json-c-config -DCMAKE_C_COMPILER=clang \
  -DBUILD_SHARED_LIBS=OFF -DBUILD_APPS=OFF -DBUILD_TESTING=OFF \
  -DDISABLE_JSON_POINTER=ON -DDISABLE_JSON_PATCH=ON > /dev/null
common='-std=gnu11 -O1 -g -fno-omit-frame-pointer -D_GNU_SOURCE'
includes='-I/work/json-c-config -I/work/json-c-src'
sources='arraylist.c debug.c json_c_version.c json_object.c json_object_iterator.c
  json_tokener.c json_util.c json_visit.c linkhash.c printbuf.c random_seed.c strerror_override.c'
files=''
for name in $sources; do files="$files /work/json-c-src/$name"; done
clang $common $includes -fprofile-instr-generate -fcoverage-mapping \
  /work/harness.c /work/replay.c $files -lm -o /work/replay
clang $common $includes -fsanitize=fuzzer,address,undefined \
  /work/harness.c $files -lm -o /work/fuzzer
