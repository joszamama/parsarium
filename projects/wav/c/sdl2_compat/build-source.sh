#!/bin/sh
set -eu
cmake -S /work/sdl3 -B /work/sdl3-build \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_SHARED_LINKER_FLAGS=-fprofile-instr-generate \
  -DCMAKE_INSTALL_PREFIX=/work/install \
  -DSDL_SHARED=ON -DSDL_STATIC=OFF -DSDL_UNIX_CONSOLE_BUILD=ON \
  -DSDL_TESTS=OFF -DSDL_EXAMPLES=OFF -DSDL_X11=OFF -DSDL_WAYLAND=OFF \
  -DSDL_KMSDRM=OFF -DSDL_RPI=OFF -DSDL_ROCKCHIP=OFF -DSDL_VULKAN=OFF \
  -DSDL_OPENGL=OFF -DSDL_OPENGLES=OFF -DSDL_ALSA=OFF -DSDL_PULSEAUDIO=OFF \
  -DSDL_JACK=OFF -DSDL_SNDIO=OFF -DSDL_OSS=OFF
cmake --build /work/sdl3-build --parallel 6 --target SDL3-shared SDL3_test
cmake --install /work/sdl3-build
cmake -S /work/compat -B /work/compat-build \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_SHARED_LINKER_FLAGS=-fprofile-instr-generate \
  -DCMAKE_PREFIX_PATH=/work/install -DCMAKE_INSTALL_PREFIX=/work/install \
  -DSDL2COMPAT_TESTS=OFF -DSDL2COMPAT_X11=OFF
cmake --build /work/compat-build --parallel 6
cmake --install /work/compat-build
