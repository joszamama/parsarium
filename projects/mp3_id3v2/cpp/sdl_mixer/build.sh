#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/sdl-source -B /work/sdl-build -DSDL_SHARED=OFF -DSDL_STATIC=ON -DSDL_TEST=OFF \
 -DSDL_TESTS=OFF -DSDL_X11=OFF -DSDL_WAYLAND=OFF -DSDL_KMSDRM=OFF \
 -DSDL_VULKAN=OFF -DSDL_OPENGL=OFF -DSDL_OPENGLES=OFF \
 -DSDL_ALSA=OFF -DSDL_PULSEAUDIO=OFF -DSDL_JACK=OFF -DSDL_SNDIO=OFF -DSDL_OSS=OFF
cmake --build /work/sdl-build -j 4
cmake --install /work/sdl-build --prefix /work/sdl-install
CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/mix-build -DCMAKE_PREFIX_PATH=/work/sdl-install \
 -DBUILD_SHARED_LIBS=OFF -DSDL2MIXER_VENDORED=OFF -DSDL2MIXER_SAMPLES=OFF \
 -DSDL2MIXER_CMD=OFF -DSDL2MIXER_FLAC=OFF -DSDL2MIXER_GME=OFF \
 -DSDL2MIXER_MOD=OFF -DSDL2MIXER_MIDI=OFF -DSDL2MIXER_OPUS=OFF \
 -DSDL2MIXER_VORBIS=OFF -DSDL2MIXER_WAVPACK=OFF \
 -DSDL2MIXER_MP3=ON -DSDL2MIXER_MP3_MINIMP3=ON -DSDL2MIXER_MP3_MPG123=OFF \
 -DSDL2MIXER_WAVE=ON
cmake --build /work/mix-build --target SDL2_mixer -j 4
sdl=$(find /work/sdl-build -name libSDL2.a -print -quit)
mix=$(find /work/mix-build -name libSDL2_mixer.a -print -quit)
test -n "$sdl" && test -n "$mix"
common='-O1 -g -fno-omit-frame-pointer -I/work/source/include -I/work/sdl-source/include -I/work/sdl-build/include'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp "$mix" "$sdl" -lm -ldl -lpthread -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness.cpp "$mix" "$sdl" -lm -ldl -lpthread -o /work/fuzzer
