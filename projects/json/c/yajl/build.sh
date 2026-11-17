#!/bin/sh
set -eu
# yajl's CMake build copies src/api/*.h into yajl/ and fills yajl_version.h; do the same here.
mkdir -p /work/yajl-inc/yajl
cp /work/yajl-src/src/api/yajl_common.h /work/yajl-src/src/api/yajl_parse.h /work/yajl-inc/yajl/
sed -e 's/${YAJL_MAJOR}/2/' -e 's/${YAJL_MINOR}/1/' -e 's/${YAJL_MICRO}/0/' \
  /work/yajl-src/src/api/yajl_version.h.cmake > /work/yajl-inc/yajl/yajl_version.h
common='-std=c99 -O1 -g -fno-omit-frame-pointer -I/work/yajl-inc -I/work/yajl-src/src -I/work'
names='yajl yajl_alloc yajl_buf yajl_encode yajl_lex yajl_parser'
srcs=''
for n in $names; do srcs="$srcs /work/yajl-src/src/$n.c"; done
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c $srcs -lm -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: only the pinned yajl lexer, parser and helper sources are instrumented.
  # CLASSIC edge instrumentation: with AFL++ 4.33c's default PCGUARD mode on arm64 the -O1
  # yajl_do_parse load of its guard index reads input bytes and the probe crashes on both valid
  # controls; the coverage, ASan/UBSan and CLASSIC builds parse them normally.
  export AFL_LLVM_INSTRUMENT=CLASSIC
  mkdir -p /work/afl-obj
  for n in $names; do
    AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -c /work/yajl-src/src/$n.c -o /work/afl-obj/$n.o
  done
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -c /work/parser-probe.c -o /work/afl-obj/parser-probe.o
  for object in /work/afl-obj/*.o; do
    if nm "$object" | grep -q '__afl_area_ptr'; then echo "$(basename "$object")"; fi
  done > /work/afl-instrumented-objects.txt
  test "$(tr '\n' ' ' < /work/afl-instrumented-objects.txt)" = "yajl.o yajl_alloc.o yajl_buf.o yajl_encode.o yajl_lex.o yajl_parser.o "
  clang /work/afl-obj/*.o -lm -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.c $srcs -lm -o /work/fuzzer
  clang $common -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.c $srcs -lm -o /work/parser-probe
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
