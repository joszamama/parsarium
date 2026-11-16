#!/bin/sh
set -eu
mkdir -p /work/deps /work/include/finwo /work/include/tidwall
fetch() {
    name="$1"; url="$2"; expected="$3"
    curl --fail --location --retry 3 "$url" -o "/work/$name.tar.gz"
    echo "$expected  /work/$name.tar.gz" | sha256sum --check
    mkdir "/work/deps/$name"
    tar -xzf "/work/$name.tar.gz" -C "/work/deps/$name" --strip-components=1
}
fetch asprintf https://github.com/finwo/c-asprintf/archive/528da9add83c8f3b073e68ed10278c378f9581a9.tar.gz 88cf53a8644dc32ae10e9b631f43aec2710d404b90f1c7b1e53d9c9fb076cd7f
fetch mindex https://github.com/finwo/c-mindex/archive/406f947a21f86e3f938fe784b279f3fe021b0d81.tar.gz 2d87d27716e740cdcb8382ae5d31b010146529722b89084822ec19af94394a09
fetch strextra https://github.com/finwo/c-strextra/archive/01f0c0070df1628edc3578b4b3a507cf4072ca79.tar.gz 6bed3fef1be1ec5d108468a841f3078a2fc61d75de30efead4d0960ef23ae7d7
fetch buf https://github.com/tidwall/buf.c/archive/b997d36cdc3fff08c49cc8d1192b5fc1c5768c9b.tar.gz d5ec4765c814921f617970e121e47d91a4bf7a2c92b8b48c41c0325446994f92
cp /work/deps/asprintf/src/asprintf.h /work/include/finwo/asprintf.h
cp /work/deps/mindex/src/mindex.h /work/include/finwo/mindex.h
cp /work/deps/strextra/src/strnstr.h /work/include/finwo/strnstr.h
cp /work/deps/buf/buf.h /work/include/tidwall/buf.h
