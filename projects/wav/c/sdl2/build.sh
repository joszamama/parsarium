#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/sdl-build -DSDL_SHARED=OFF -DSDL_STATIC=ON -DSDL_TEST=OFF \
 -DSDL_TESTS=OFF -DSDL_X11=OFF -DSDL_WAYLAND=OFF \
 -DSDL_KMSDRM=OFF -DSDL_RPI=OFF -DSDL_ROCKCHIP=OFF -DSDL_VULKAN=OFF \
 -DSDL_OPENGL=OFF -DSDL_OPENGLES=OFF -DSDL_ALSA=OFF -DSDL_PULSEAUDIO=OFF \
 -DSDL_JACK=OFF -DSDL_SNDIO=OFF -DSDL_OSS=OFF
cmake --build /work/sdl-build --target SDL2-static -j 4
library=$(find /work/sdl-build -name libSDL2.a -print -quit)
test -n "$library"
common='-O1 -g -fno-omit-frame-pointer -I/work/source/include -I/work/sdl-build/include'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c "$library" -lm -ldl -lpthread -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c "$library" -lm -ldl -lpthread -o /work/fuzzer
