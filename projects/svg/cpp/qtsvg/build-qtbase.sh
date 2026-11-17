#!/bin/sh
set -eu
cmake -S /work/qtbase -B /work/qtbase-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/work/qt \
  -DQT_BUILD_TESTS=OFF -DQT_BUILD_EXAMPLES=OFF \
  -DFEATURE_sql=OFF -DFEATURE_network=OFF -DFEATURE_dbus=OFF \
  -DFEATURE_widgets=OFF -DFEATURE_printsupport=OFF \
  -DFEATURE_xcb=OFF -DINPUT_opengl=no -DFEATURE_vulkan=OFF
cmake --build /work/qtbase-build -j 4
cmake --install /work/qtbase-build
