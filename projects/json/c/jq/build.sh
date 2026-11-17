#!/bin/sh
set -eu
# Build libjq (no oniguruma, bundled decNumber) in tree, once per instrumentation.
common='-O1 -g -fno-omit-frame-pointer'
build_libjq() {
  cd /work/jq-src
  # jq's distclean recurses into the unconfigured oniguruma tree, so remove objects directly.
  rm -rf .libs libjq.la src/*.o src/*.lo src/.libs vendor/decNumber/*.o vendor/decNumber/*.lo vendor/decNumber/.libs
  ./configure CC=clang CFLAGS="$1" --disable-docs --with-oniguruma=no --disable-shared --enable-static > /work/configure.log
  make src/builtin.inc src/config_opts.inc src/version.h > /dev/null
  make -j4 libjq.la > /work/make.log
  cd /work
}
include='-I/work/jq-src/src -I/work'
build_libjq "$common -fprofile-instr-generate -fcoverage-mapping"
clang $common $include -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/jq-src/.libs/libjq.a -lm -lpthread -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: libjq's JSON reader and jv value sources only.
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  build_libjq "$common"
  clang $common $include -c /work/parser-probe.c -o /work/parser-probe.o
  for object in /work/jq-src/src/*.o /work/jq-src/vendor/decNumber/*.o /work/parser-probe.o; do
    if nm "$object" | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "$(basename "$object")"; fi
  done > /work/afl-instrumented-objects.txt
  test "$(tr '\n' ' ' < /work/afl-instrumented-objects.txt)" = "jv.o jv_alloc.o jv_dtoa.o jv_parse.o jv_unicode.o "
  clang /work/parser-probe.o /work/jq-src/.libs/libjq.a -lm -lpthread -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang $common $include -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.c /work/jq-src/.libs/libjq.a -lm -lpthread -o /work/parser-probe
  build_libjq "$common -fsanitize=fuzzer-no-link,address,undefined"
  clang $common $include -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.c /work/jq-src/.libs/libjq.a -lm -lpthread -o /work/fuzzer
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
