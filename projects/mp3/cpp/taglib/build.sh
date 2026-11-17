#!/bin/sh
set -eu
src=/work/taglib-2.3.2
common='-O1 -g -fno-omit-frame-pointer'
opts='-DBUILD_SHARED_LIBS=OFF -DBUILD_TESTING=OFF -DBUILD_BINDINGS=ON -DWITH_ZLIB=OFF -DWITH_APE=OFF -DWITH_ASF=OFF -DWITH_DSF=OFF -DWITH_MATROSKA=OFF -DWITH_MOD=OFF -DWITH_RIFF=OFF -DWITH_SHORTEN=OFF -DWITH_TRUEAUDIO=OFF -DWITH_VORBIS=OFF'
inc='-I/work/taglib-2.3.2/taglib -I/work/taglib-2.3.2/taglib/mpeg -I/work/taglib-2.3.2/taglib/mpeg/id3v2 -I/work/taglib-2.3.2/taglib/toolkit -I/work/coverage-build'
cmake -S "$src" -B /work/coverage-build -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_CXX_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" $opts
cmake --build /work/coverage-build --target tag_c -j 2
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping $inc /work/harness.cpp /work/replay.cpp /work/coverage-build/taglib/libtag.a -lm -o /work/replay
cmake -S "$src" -B /work/fuzz-build -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_CXX_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" $opts
cmake --build /work/fuzz-build --target tag_c -j 2
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined $inc /work/harness.cpp /work/fuzz-build/taglib/libtag.a -lm -o /work/fuzzer
