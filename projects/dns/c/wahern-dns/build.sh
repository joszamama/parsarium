#!/bin/sh
set -eu
# dns.c is a single-file library: compile src/dns.c as the library object with the
# upstream Makefile's -std=gnu99 (without DNS_MAIN, so its command-line driver is left out).
common='-std=gnu99 -O1 -g -fno-omit-frame-pointer'
build() {
    dir=$1; flags=$2
    mkdir -p "$dir"
    cp /work/dns-src/src/dns.c /work/dns-src/src/dns.h "$dir"/
    clang $common $flags -c "$dir/dns.c" -o "$dir/dns.o"
}
build /work/build-cov '-fprofile-instr-generate -fcoverage-mapping'
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/build-cov \
    /work/harness.c /work/build-cov/dns.o -o /work/replay
build /work/build-fuzz '-fsanitize=fuzzer-no-link,address,undefined'
clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined -I/work/build-fuzz \
    /work/harness.c /work/build-fuzz/dns.o -o /work/fuzzer
