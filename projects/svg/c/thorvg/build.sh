#!/bin/sh
set -eu
options='--buildtype=plain -Dstrip=false -Ddefault_library=static -Dengines=cpu -Dloaders=svg -Dsavers= -Dbindings=capi -Dtools= -Dextra= -Dthreads=false -Dsimd=false -Dfile=true -Dlog=false -Dtests=false'
common='-O1 -g -fno-omit-frame-pointer'
CXX=clang++ CXXFLAGS="$common -fprofile-instr-generate -fcoverage-mapping" LDFLAGS='-fprofile-instr-generate' \
 meson setup /work/build-cov /work/source $options
meson compile -C /work/build-cov -j 4
CXX=clang++ CXXFLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" LDFLAGS='-fsanitize=address,undefined' \
 meson setup /work/build-fuzz /work/source $options
meson compile -C /work/build-fuzz -j 4
cov=$(find /work/build-cov -name libthorvg-1.a -print -quit)
fuzz=$(find /work/build-fuzz -name libthorvg-1.a -print -quit)
test -n "$cov" && test -n "$fuzz"
include='-I/work/source/src/bindings/capi -DTVG_STATIC'
clang $common $include -fprofile-instr-generate -fcoverage-mapping -c /work/harness.c -o /work/harness-cov.o
clang $common $include -fprofile-instr-generate -fcoverage-mapping -c /work/replay.c -o /work/replay.o
clang++ $common -fprofile-instr-generate /work/harness-cov.o /work/replay.o "$cov" -lm -lpthread -o /work/replay
clang $common $include -fsanitize=fuzzer,address,undefined -c /work/harness.c -o /work/harness-fuzz.o
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness-fuzz.o "$fuzz" -lm -lpthread -o /work/fuzzer
