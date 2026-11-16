#!/bin/sh
set -eu
options='-DBUILD_SHARED_LIBS=OFF -DSAIL_ONLY_CODECS=pnm -DSAIL_BUILD_APPS=OFF -DSAIL_BUILD_BINDINGS=OFF -DSAIL_BUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF -DSAIL_ENABLE_OPENMP=OFF -DSAIL_MANIP_USE_SWSCALE=OFF'
cmake -S /work/source -B /work/build-cov -DCMAKE_C_COMPILER=clang -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' $options
cmake --build /work/build-cov -j4
cmake -S /work/source -B /work/build-fuzz -DCMAKE_C_COMPILER=clang -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_FLAGS='-O1 -g -fsanitize=fuzzer-no-link,address,undefined' $options
cmake --build /work/build-fuzz -j4
covlibs='/work/build-cov/src/sail/libsail.a /work/build-cov/src/sail-manip/libsail-manip.a /work/build-cov/src/sail-codecs-archive/libsail-codecs.a /work/build-cov/src/sail-common/libsail-common.a'
fuzzlibs='/work/build-fuzz/src/sail/libsail.a /work/build-fuzz/src/sail-manip/libsail-manip.a /work/build-fuzz/src/sail-codecs-archive/libsail-codecs.a /work/build-fuzz/src/sail-common/libsail-common.a'
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping -I/work/source/src -I/work/build-cov/include /work/harness.c /work/replay.c $covlibs -o /work/replay
clang -O1 -g -fsanitize=fuzzer,address,undefined -I/work/source/src -I/work/build-fuzz/include /work/harness.c $fuzzlibs -o /work/fuzzer
