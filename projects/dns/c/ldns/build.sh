#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
build() {
    dir=$1; flags=$2
    cp -a /work/ldns-src "$dir"
    cd "$dir"
    ./configure CC=clang CFLAGS="$common $flags" --disable-shared --enable-static --without-ssl --disable-sha2 \
        --disable-dane --disable-gost --disable-ecdsa --disable-ed25519 --disable-ed448 \
        --without-drill --without-examples --without-pyldns --without-pyldnsx --without-p5-dns-ldns > /dev/null
    make -j4 lib > /dev/null
    cd /work
}
build /work/build-cov '-fprofile-instr-generate -fcoverage-mapping'
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/build-cov \
    /work/harness.c /work/build-cov/.libs/libldns.a -o /work/replay
build /work/build-fuzz '-fsanitize=fuzzer-no-link,address,undefined'
clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined -I/work/build-fuzz \
    /work/harness.c /work/build-fuzz/.libs/libldns.a -o /work/fuzzer
