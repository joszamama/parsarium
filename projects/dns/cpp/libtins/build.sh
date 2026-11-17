#!/bin/sh
set -eu
src=/work/libtins-src
common='-O1 -g -fno-omit-frame-pointer'
build() {
    dir=$1; flags=$2
    cmake -S "$src" -B "$dir" -G Ninja -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang \
        -DCMAKE_BUILD_TYPE=None -DCMAKE_CXX_FLAGS="$common $flags" \
        -DLIBTINS_BUILD_SHARED=OFF -DLIBTINS_ENABLE_PCAP=OFF -DLIBTINS_BUILD_EXAMPLES=OFF \
        -DLIBTINS_BUILD_TESTS=OFF -DLIBTINS_ENABLE_DOT11=OFF -DLIBTINS_ENABLE_WPA2=OFF \
        -DLIBTINS_ENABLE_ACK_TRACKER=OFF -DLIBTINS_ENABLE_TCP_STREAM_CUSTOM_DATA=OFF > /dev/null
    cmake --build "$dir" > /dev/null
}
build /work/build-cov '-fprofile-instr-generate -fcoverage-mapping'
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping -I$src/include -I/work/build-cov/include \
    /work/harness.cpp /work/build-cov/lib/libtins.a -o /work/replay
build /work/build-fuzz '-fsanitize=fuzzer-no-link,address,undefined'
clang++ -std=c++17 $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined -I$src/include -I/work/build-fuzz/include \
    /work/harness.cpp /work/build-fuzz/lib/libtins.a -o /work/fuzzer
