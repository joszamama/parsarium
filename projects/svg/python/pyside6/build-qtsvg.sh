#!/bin/sh
# QtSvg 6.12.0 with LLVM source coverage, built against the plain qtbase 6.12.0 build.
set -eu
flags='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
CC=clang CXX=clang++ CFLAGS="$flags" CXXFLAGS="$flags" \
 cmake -S /work/source -B /work/build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_PREFIX_PATH=/work/qt -DCMAKE_INSTALL_PREFIX=/work/qt \
  -DCMAKE_SHARED_LINKER_FLAGS=-fprofile-instr-generate \
  -DQT_BUILD_TESTS=OFF -DQT_BUILD_EXAMPLES=OFF
cmake --build /work/build -j 4
cmake --install /work/build
