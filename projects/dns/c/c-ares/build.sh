#!/bin/sh
set -eu
src=/work/c-ares-src
common='-O1 -g -fno-omit-frame-pointer'
build() {
    dir=$1; flags=$2
    cmake -S "$src" -B "$dir" -G Ninja -DCMAKE_C_COMPILER=clang -DCMAKE_BUILD_TYPE=None \
        -DCMAKE_C_FLAGS="$common $flags" -DCARES_STATIC=ON -DCARES_SHARED=OFF \
        -DCARES_BUILD_TOOLS=OFF -DCARES_BUILD_TESTS=OFF -DCARES_INSTALL=OFF -DCARES_THREADS=OFF > /dev/null
    cmake --build "$dir" > /dev/null
}
build /work/build-cov '-fprofile-instr-generate -fcoverage-mapping'
clang $common -fprofile-instr-generate -fcoverage-mapping -I$src/include -I/work/build-cov \
    /work/harness.c /work/build-cov/lib/libcares.a -o /work/replay
build /work/build-fuzz '-fsanitize=fuzzer-no-link,address,undefined'
clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined -I$src/include -I/work/build-fuzz \
    /work/harness.c /work/build-fuzz/lib/libcares.a -o /work/fuzzer
