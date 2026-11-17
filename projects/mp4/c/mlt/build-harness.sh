#!/bin/sh
set -eu
mode=${PARSARIUM_BUILD:-coverage}
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer -I/work/install/include/mlt-7'
libs='-L/work/install/lib -Wl,-rpath,/work/install/lib -lmlt-7 -lm -lpthread -ldl'
case "$mode" in
coverage)
  clang $common -fprofile-instr-generate -fcoverage-mapping \
    /work/harness.c /work/replay.c $libs -o /work/replay
  clang $common -fsanitize=fuzzer,address,undefined \
    /work/harness.c $libs -o /work/fuzzer
  ;;
afl)
  printf 'src:mov.c\n' > /work/afl-allowlist.txt
  export AFL_LLVM_INSTRUMENT=CLASSIC AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  afl-clang-fast $common /work/harness.c /work/replay.c $libs -o /work/replay
  afl-clang-fast $common -fsanitize=fuzzer,address,undefined -fno-sanitize=function \
    /work/harness.c $libs -o /work/fuzzer
  ;;
*) echo "unknown PARSARIUM_BUILD: $mode" >&2; exit 2 ;;
esac
