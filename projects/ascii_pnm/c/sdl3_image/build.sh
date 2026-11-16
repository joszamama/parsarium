#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/sdl-source -B /work/sdl-build -DSDL_SHARED=OFF -DSDL_STATIC=ON -DSDL_UNIX_CONSOLE_BUILD=ON \
 -DSDL_TESTS=OFF -DSDL_TEST_LIBRARY=OFF -DSDL_EXAMPLES=OFF -DSDL_X11=OFF -DSDL_WAYLAND=OFF \
 -DSDL_KMSDRM=OFF -DSDL_RPI=OFF -DSDL_ROCKCHIP=OFF -DSDL_VULKAN=OFF \
 -DSDL_OPENGL=OFF -DSDL_OPENGLES=OFF -DSDL_ALSA=OFF -DSDL_PULSEAUDIO=OFF \
 -DSDL_JACK=OFF -DSDL_SNDIO=OFF -DSDL_OSS=OFF
cmake --build /work/sdl-build --target SDL3-static -j 4
cmake --install /work/sdl-build --prefix /work/sdl-install
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/img-build -DCMAKE_PREFIX_PATH=/work/sdl-install \
 -DBUILD_SHARED_LIBS=OFF -DSDLIMAGE_SAMPLES=OFF -DSDLIMAGE_TESTS=OFF \
 -DSDLIMAGE_VENDORED=OFF -DSDLIMAGE_AVIF=OFF -DSDLIMAGE_JPG=OFF \
 -DSDLIMAGE_JXL=OFF -DSDLIMAGE_TIF=OFF -DSDLIMAGE_WEBP=OFF \
 -DSDLIMAGE_PNG=ON -DSDLIMAGE_PNG_LIBPNG=OFF -DSDLIMAGE_PNM=ON -DSDLIMAGE_SVG=ON
cmake --build /work/img-build --target SDL3_image-static -j 4
sdl=$(find /work/sdl-build -name libSDL3.a -print -quit)
img=$(find /work/img-build -name libSDL3_image.a -print -quit)
test -n "$sdl" && test -n "$img"
common='-O1 -g -fno-omit-frame-pointer -I/work/source/include -I/work/sdl-source/include -I/work/sdl-build/include'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c "$img" "$sdl" -lm -ldl -lpthread -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c "$img" "$sdl" -lm -ldl -lpthread -o /work/fuzzer
