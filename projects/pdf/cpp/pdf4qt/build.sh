#!/bin/sh
set -eu

cmake -S /work/blend2d -B /work/blend-build -G Ninja \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/work/install \
  -DCMAKE_INSTALL_LIBDIR=lib -DBLEND2D_NO_JIT=ON \
  -DBLEND2D_TEST=OFF -DBLEND2D_DEMOS=OFF
cmake --build /work/blend-build --parallel 4
cmake --install /work/blend-build
test -f /work/install/lib/libblend2d.so

cmake -S /work/source -B /work/build -G Ninja \
  -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_CXX_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_SHARED_LINKER_FLAGS='-fprofile-instr-generate' \
  -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib \
  -DCMAKE_PREFIX_PATH=/work/install \
  -DPDF4QT_BUILD_ONLY_CORE_LIBRARY=ON -DPDF4QT_BUILD_TESTS=OFF \
  -DPDF4QT_INSTALL_TO_USR=OFF -DPDF4QT_INSTALL_DEPENDENCIES=OFF
cmake --build /work/build --target Pdf4QtLibCore --parallel 4
cp -a /work/build/lib/libPdf4QtLibCore.so* /work/install/lib/
test -f /work/install/lib/libPdf4QtLibCore.so

qt_flags=$(pkg-config --cflags --libs Qt6Core Qt6Gui Qt6Svg Qt6Xml)
clang++ -std=c++20 -O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping \
  -I/work/source/Pdf4QtLibCore/sources -I/work/build /work/harness.cpp /work/replay.cpp \
  $qt_flags -L/work/install/lib -lPdf4QtLibCore -Wl,-rpath,/work/install/lib -o /work/replay
clang++ -std=c++20 -O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer,address,undefined \
  -I/work/source/Pdf4QtLibCore/sources -I/work/build /work/harness.cpp \
  $qt_flags -L/work/install/lib -lPdf4QtLibCore -Wl,-rpath,/work/install/lib -o /work/fuzzer
