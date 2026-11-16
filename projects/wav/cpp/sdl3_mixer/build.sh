#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/sdl-source -B /work/sdl-build -DSDL_SHARED=OFF -DSDL_STATIC=ON -DSDL_UNIX_CONSOLE_BUILD=ON -DSDL_TEST_LIBRARY=OFF \
 -DSDL_TESTS=OFF -DSDL_X11=OFF -DSDL_WAYLAND=OFF -DSDL_KMSDRM=OFF \
 -DSDL_VULKAN=OFF -DSDL_OPENGL=OFF -DSDL_OPENGLES=OFF \
 -DSDL_ALSA=OFF -DSDL_PULSEAUDIO=OFF -DSDL_JACK=OFF -DSDL_SNDIO=OFF -DSDL_OSS=OFF
cmake --build /work/sdl-build -j 4
cmake --install /work/sdl-build --prefix /work/sdl-install
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/mix-build -DCMAKE_PREFIX_PATH=/work/sdl-install \
 -DBUILD_SHARED_LIBS=OFF -DSDLMIXER_VENDORED=OFF -DSDLMIXER_TESTS=OFF -DSDLMIXER_EXAMPLES=OFF \
 -DSDLMIXER_WAVE=ON -DSDLMIXER_AIFF=OFF -DSDLMIXER_VOC=OFF -DSDLMIXER_AU=OFF \
 -DSDLMIXER_FLAC=OFF -DSDLMIXER_GME=OFF -DSDLMIXER_MOD=OFF \
 -DSDLMIXER_MP3=OFF -DSDLMIXER_MIDI=OFF -DSDLMIXER_OPUS=OFF \
 -DSDLMIXER_VORBIS_STB=OFF -DSDLMIXER_VORBIS_VORBISFILE=OFF \
 -DSDLMIXER_VORBIS_TREMOR=OFF -DSDLMIXER_WAVPACK=OFF
cmake --build /work/mix-build --target SDL3_mixer-static -j 4
sdl=$(find /work/sdl-build -name libSDL3.a -print -quit)
mix=$(find /work/mix-build -name 'libSDL3_mixer*.a' -print -quit)
test -n "$sdl" && test -n "$mix"
common='-O1 -g -fno-omit-frame-pointer -I/work/source/include -I/work/sdl-source/include -I/work/sdl-build/include'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp "$mix" "$sdl" -lm -ldl -lpthread -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness.cpp "$mix" "$sdl" -lm -ldl -lpthread -o /work/fuzzer
