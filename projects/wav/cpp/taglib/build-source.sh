#!/bin/sh
set -eu
cmake -S /work/source/taglib -B /work/build/taglib -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_CXX_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_INSTALL_PREFIX=/work/install -DBUILD_SHARED_LIBS=ON -DBUILD_BINDINGS=ON \
  -DWITH_APE=OFF -DWITH_ASF=OFF -DWITH_DSF=OFF -DWITH_MATROSKA=OFF \
  -DWITH_MOD=OFF -DWITH_MP4=OFF -DWITH_RIFF=ON -DWITH_SHORTEN=OFF \
  -DWITH_TRUEAUDIO=OFF -DWITH_VORBIS=OFF -DWITH_ZLIB=OFF
cmake --build /work/build/taglib -j 6
cmake --install /work/build/taglib
