#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
build() {
    dir=$1; flags=$2
    cp -a /work/udns-src "$dir"
    cd "$dir"
    CC=clang CFLAGS="$common $flags" ./configure > /dev/null
    make staticlib > /dev/null
    cd /work
}
build /work/build-cov '-fprofile-instr-generate -fcoverage-mapping'
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/build-cov \
    /work/harness.c /work/build-cov/libudns.a -o /work/replay
build /work/build-fuzz '-fsanitize=fuzzer-no-link,address,undefined'
clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined -I/work/build-fuzz \
    /work/harness.c /work/build-fuzz/libudns.a -o /work/fuzzer
