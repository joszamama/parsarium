#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
deps="$(pkg-config --libs gnutls liburcu) -lpthread -lm"
build() {
    dir=$1; flags=$2
    cp -a /work/knot-src "$dir"
    cd "$dir"
    ./configure CC=clang CFLAGS="$common $flags" --disable-shared --enable-static --disable-daemon \
        --disable-modules --disable-utilities --disable-documentation --disable-fastparser \
        --enable-quic=no --enable-xdp=no --enable-redis=no --enable-systemd=no --enable-dbus=no \
        --enable-cap-ng=no --enable-maxminddb=no --with-lmdb=embedded --with-libidn=no --with-libnghttp2=no > /dev/null
    make -j4 -C src libknot.la > /dev/null
    cd /work
}
build /work/build-cov '-fprofile-instr-generate -fcoverage-mapping'
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/build-cov/src \
    /work/harness.c /work/build-cov/src/.libs/libknot.a $deps -o /work/replay
build /work/build-fuzz '-fsanitize=fuzzer-no-link,address,undefined'
clang $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined -I/work/build-fuzz/src \
    /work/harness.c /work/build-fuzz/src/.libs/libknot.a $deps -o /work/fuzzer
