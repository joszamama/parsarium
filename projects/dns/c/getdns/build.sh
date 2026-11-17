#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
deps='-lssl -lcrypto -lpthread'
build() {
    dir=$1; flags=$2
    cmake -S /work/getdns-src -B "$dir" -DCMAKE_C_COMPILER=clang -DCMAKE_BUILD_TYPE=None \
        -DCMAKE_C_FLAGS="$common $flags" -DENABLE_SHARED=OFF -DENABLE_STATIC=ON -DENABLE_STUB_ONLY=ON \
        -DBUILD_GETDNS_QUERY=OFF -DBUILD_GETDNS_SERVER_MON=OFF -DBUILD_STUBBY=OFF -DBUILD_EXAMPLES=OFF \
        -DBUILD_LIBEV=OFF -DBUILD_LIBEVENT2=OFF -DBUILD_LIBUV=OFF -DUSE_LIBIDN2=OFF -DBUILD_TESTING=OFF \
        -DBUILD_DOXYGEN=OFF > /dev/null
    cmake --build "$dir" -j4 --target getdns > /dev/null
}
build /work/build-cov '-fprofile-instr-generate -fcoverage-mapping'
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/build-cov \
    /work/harness.c /work/build-cov/libgetdns.a $deps -o /work/replay
build /work/build-fuzz '-fsanitize=fuzzer-no-link,address,undefined'
clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined -I/work/build-fuzz \
    /work/harness.c /work/build-fuzz/libgetdns.a $deps -o /work/fuzzer
