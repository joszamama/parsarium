#!/bin/sh
set -eu
cd /work/libfastjson-src
./configure CC=clang --disable-shared --enable-static > /work/configure.log
cd /work
common='-std=gnu11 -O1 -g -fno-omit-frame-pointer -DHAVE_CONFIG_H -I/work/libfastjson-src -I/work'
lib='arraylist.c debug.c json_object.c json_object_iterator.c json_print.c json_tokener.c json_util.c json_version.c printbuf.c'
src=''
for name in $lib; do src="$src /work/libfastjson-src/$name"; done
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c $src -lm -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: tokener, object tree, array list and string buffer only.
  mkdir -p /work/afl-obj
  for name in $lib; do
    AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -c /work/libfastjson-src/$name -o /work/afl-obj/${name%.c}.o
  done
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -c /work/parser-probe.c -o /work/afl-obj/parser-probe.o
  for object in /work/afl-obj/*.o; do
    if nm "$object" | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "$(basename "$object")"; fi
  done > /work/afl-instrumented-objects.txt
  test "$(tr '\n' ' ' < /work/afl-instrumented-objects.txt)" = "arraylist.o json_object.o json_tokener.o printbuf.o "
  clang /work/afl-obj/*.o -lm -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.c $src -lm -o /work/fuzzer
  clang $common -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.c $src -lm -o /work/parser-probe
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
