#!/bin/sh
set -eu
set --
for path in /work/source/src/*.imageio; do
    name=${path##*/}
    name=${name%.imageio}
    if [ "$name" != pnm ]; then
        set -- "$@" "-DENABLE_$name=OFF"
    fi
done
CC=clang CXX=clang++ CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo \
 -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib \
 -DOpenColorIO_DIR=/usr/lib/aarch64-linux-gnu/cmake/OpenColorIO \
 -DBUILD_SHARED_LIBS=ON -DEMBEDPLUGINS=ON -DOIIO_BUILD_TOOLS=OFF \
 -DOIIO_BUILD_TESTS=OFF -DBUILD_TESTING=OFF -DBUILD_DOCS=OFF -DINSTALL_DOCS=OFF \
 -DUSE_PYTHON=OFF -DUSE_QT=OFF -DUSE_SIMD=0 "$@"
cmake --build /work/build -j 4
cmake --install /work/build
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags OpenImageIO) /work/harness.cpp /work/replay.cpp $(pkg-config --libs OpenImageIO) -Wl,-rpath,/work/install/lib -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags OpenImageIO) /work/harness.cpp $(pkg-config --libs OpenImageIO) -Wl,-rpath,/work/install/lib -o /work/fuzzer
