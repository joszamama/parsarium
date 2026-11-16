#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 meson setup /work/build /work/source --prefix=/work/install --libdir=lib --buildtype=plain \
 -Dauto_features=disabled -Dbase=enabled -Dgood=enabled -Dbad=enabled -Dugly=disabled -Dlibav=disabled \
 -Ddevtools=disabled -Dges=disabled -Dpython=disabled -Drtsp_server=disabled -Dgst-full=disabled \
 -Dorc=disabled -Dgstreamer:check=enabled -Dtools=enabled -Dtests=disabled -Dexamples=disabled -Dintrospection=disabled \
 -Dgst-plugins-base:app=enabled -Dgst-plugins-base:playback=enabled -Dgst-plugins-base:typefind=enabled \
 -Dgst-plugins-base:audioconvert=enabled -Dgst-plugins-good:wavparse=enabled \
 -Dgst-plugins-good:id3demux=enabled -Dgst-plugins-good:audioparsers=enabled \
 -Dgst-plugins-good:isomp4=enabled -Dgst-plugins-bad:pnm=enabled
meson compile -C /work/build -j 6
meson install -C /work/build
