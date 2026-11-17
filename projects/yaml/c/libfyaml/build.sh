#!/bin/sh
set -eu
# The option is split as c""lang because the AFL++ overlay rewrites every compiler name in this file.
configure='--disable-shared --enable-static --disable-network --with-libc''lang=no'
# Replay: the whole static library with LLVM source coverage, built by its own autotools build.
cp -a /work/libfyaml-src /work/libfyaml-cov
cd /work/libfyaml-cov
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' ./configure $configure > /work/configure-cov.log
make -C src -j4 libfyaml.la > /work/make-cov.log
cd /work
common='-std=gnu11 -O1 -g -fno-omit-frame-pointer -I/work/libfyaml-src/include -I/work'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c \
    /work/libfyaml-cov/src/.libs/libfyaml.a -lm -lpthread -o /work/replay
if dpkg-query -W -f='${Status}' afl++ 2>/dev/null | grep -q 'install ok installed'; then
  # Parser-scoped AFL++ map: only the libfyaml src/lib parser, composer and document sources are instrumented.
  cp -a /work/libfyaml-src /work/libfyaml-afl
  cd /work/libfyaml-afl
  CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer' ./configure $configure > /work/configure-afl.log
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt make -C src -j4 libfyaml.la > /work/make-afl.log
  cd /work
  AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt clang $common -c /work/parser-probe.c -o /work/parser-probe.o
  for object in $(find /work/libfyaml-afl/src -name "*.o") /work/parser-probe.o; do
    if nm "$object" | grep -q '__sanitizer_cov_trace_pc_guard'; then echo "$(basename "$object")"; fi
  done | sort > /work/afl-instrumented-objects.txt
  cat /work/afl-instrumented-objects.txt >&2
  # Every instrumented object is a src/lib source; util, allocator, xxhash, blake3 and the probe are not.
  test "$(wc -l < /work/afl-instrumented-objects.txt)" -eq "$(grep -c "^src:" /work/afl-allowlist.txt)"
  ! grep -v '^libfyaml_la-fy-' /work/afl-instrumented-objects.txt
  clang /work/parser-probe.o /work/libfyaml-afl/src/.libs/libfyaml.a -lm -lpthread -o /work/parser-probe
  cp /work/parser-probe /work/fuzzer
else
  clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer /work/harness.c \
      /work/libfyaml-cov/src/.libs/libfyaml.a -lm -lpthread -o /work/fuzzer
  clang $common -fprofile-instr-generate -fcoverage-mapping /work/parser-probe.c \
      /work/libfyaml-cov/src/.libs/libfyaml.a -lm -lpthread -o /work/parser-probe
  echo 'not an AFL++ build' > /work/afl-instrumented-objects.txt
fi
