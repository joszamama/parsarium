#!/bin/sh
set -eu
# QtBase is the parser under test: QtGui's built-in QPpmHandler
# (src/gui/image/qppmhandler.cpp). Build it from the pinned archive with LLVM
# source coverage. Image-format plugins are disabled so no plugin can claim
# the "ppm" format ahead of the built-in handler.
flags='-O1 -gline-tables-only -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
LLVM_PROFILE_FILE=/tmp/qtbase-build-%p.profraw CFLAGS="$flags" CXXFLAGS="$flags" \
 cmake -S /work/source -B /work/qtbase-build -G Ninja \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/work/qt \
  -DQT_BUILD_TESTS=OFF -DQT_BUILD_EXAMPLES=OFF \
  -DFEATURE_sql=OFF -DFEATURE_network=OFF -DFEATURE_dbus=OFF \
  -DFEATURE_widgets=OFF -DFEATURE_printsupport=OFF \
  -DFEATURE_xcb=OFF -DINPUT_opengl=no -DFEATURE_vulkan=OFF \
  -DFEATURE_gif=OFF -DFEATURE_ico=OFF -DFEATURE_jpeg=OFF \
  -DFEATURE_imageformat_ppm=ON
LLVM_PROFILE_FILE=/tmp/qtbase-build-%p.profraw cmake --build /work/qtbase-build -j 4
LLVM_PROFILE_FILE=/tmp/qtbase-build-%p.profraw cmake --install /work/qtbase-build
rm -f /tmp/qtbase-build-*.profraw
common='-O1 -g -fno-omit-frame-pointer'
includes='-I/work/qt/include -I/work/qt/include/QtCore -I/work/qt/include/QtGui'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $includes /work/harness.cpp /work/replay.cpp -L/work/qt/lib -Wl,-rpath,/work/qt/lib -lQt6Gui -lQt6Core -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $includes /work/harness.cpp -L/work/qt/lib -Wl,-rpath,/work/qt/lib -lQt6Gui -lQt6Core -o /work/fuzzer
