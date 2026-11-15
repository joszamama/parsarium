#!/bin/sh
set -eu
src=/work/taglib-2.3.2
common='-O1 -g -fno-omit-frame-pointer'
opts='-DBUILD_SHARED_LIBS=OFF -DBUILD_TESTING=OFF -DBUILD_BINDINGS=ON -DWITH_ZLIB=OFF -DWITH_APE=OFF -DWITH_ASF=OFF -DWITH_DSF=OFF -DWITH_MATROSKA=OFF -DWITH_MOD=OFF -DWITH_RIFF=OFF -DWITH_SHORTEN=OFF -DWITH_TRUEAUDIO=OFF -DWITH_VORBIS=OFF'
inc='-I/work/taglib-2.3.2/bindings/c'
cmake -S "$src" -B /work/coverage-build -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_CXX_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" $opts
cmake --build /work/coverage-build --target tag_c -j 2
clang $common -fprofile-instr-generate -fcoverage-mapping $inc -c /work/harness.c -o /work/harness.o
clang $common -fprofile-instr-generate -fcoverage-mapping $inc -c /work/replay.c -o /work/replay.o
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.o /work/replay.o /work/coverage-build/bindings/c/libtag_c.a /work/coverage-build/taglib/libtag.a -lm -o /work/replay
cmake -S "$src" -B /work/fuzz-build -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_CXX_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" $opts
cmake --build /work/fuzz-build --target tag_c -j 2
clang $common -fsanitize=fuzzer-no-link,address,undefined $inc -c /work/harness.c -o /work/harness-fuzz.o
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness-fuzz.o /work/fuzz-build/bindings/c/libtag_c.a /work/fuzz-build/taglib/libtag.a -lm -o /work/fuzzer
