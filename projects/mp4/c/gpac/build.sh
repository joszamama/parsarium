#!/bin/sh
set -eu
src=/work/gpac-26.07.0
common='-O1 -g -fno-omit-frame-pointer'
cov='-fprofile-instr-generate -fcoverage-mapping'
fuzz='-fsanitize=fuzzer-no-link,address,undefined'
# Static libgpac with only the ISO media profile. Upstream ignores --use-FOO=no
# here, so optional libraries stay off because only zlib headers are installed.
opts='--static-build --isomedia-only --disable-dvb4linux --disable-doc --disable-opt'
libgpac() {
 mkdir -p "$1" && cd "$1"
 "$src/configure" --cc=clang --cxx=clang++ $opts --extra-cflags="$common $2" --extra-ldflags="$2"
 make -j 4 lib
 cd /work
}
libgpac /work/coverage-build "$cov"
inc="-DGPAC_HAVE_CONFIG_H -I/work/coverage-build -I$src/include"
libs=$(sed -n 's/^Libs.private: -lgpac_static //p' /work/coverage-build/gpac.pc)
clang -std=c11 $common $cov $inc -c /work/harness.c -o /work/harness.o
clang -std=c11 $common $cov $inc -c /work/replay.c -o /work/replay.o
clang $common $cov /work/harness.o /work/replay.o /work/coverage-build/bin/gcc/libgpac_static.a $libs -o /work/replay
libgpac /work/fuzz-build "$fuzz"
inc="-DGPAC_HAVE_CONFIG_H -I/work/fuzz-build -I$src/include"
libs=$(sed -n 's/^Libs.private: -lgpac_static //p' /work/fuzz-build/gpac.pc)
clang -std=c11 $common $fuzz $inc -c /work/harness.c -o /work/harness-fuzz.o
clang $common -fsanitize=fuzzer,address,undefined /work/harness-fuzz.o /work/fuzz-build/bin/gcc/libgpac_static.a $libs -o /work/fuzzer
