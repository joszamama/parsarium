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
 cmake -S /work/source -B /work/sound-build -DCMAKE_PREFIX_PATH=/work/sdl-install \
 -DSDLSOUND_BUILD_STATIC=ON -DSDLSOUND_BUILD_SHARED=OFF \
 -DSDLSOUND_BUILD_TEST=OFF -DSDLSOUND_BUILD_DOCS=OFF \
 -DSDLSOUND_DECODER_WAV=ON -DSDLSOUND_DECODER_MP3=ON \
 -DSDLSOUND_DECODER_AIFF=OFF -DSDLSOUND_DECODER_AU=OFF \
 -DSDLSOUND_DECODER_VOC=OFF -DSDLSOUND_DECODER_FLAC=OFF \
 -DSDLSOUND_DECODER_VORBIS=OFF -DSDLSOUND_DECODER_RAW=OFF \
 -DSDLSOUND_DECODER_SHN=OFF -DSDLSOUND_DECODER_MODPLUG=OFF
cmake --build /work/sound-build --target SDL3_sound-static -j 4
sdl=$(find /work/sdl-build -name libSDL3.a -print -quit)
sound=$(find /work/sound-build -name libSDL3_sound.a -print -quit)
test -n "$sdl" && test -n "$sound"
common='-O1 -g -fno-omit-frame-pointer -I/work/source/include -I/work/source/src -I/work/sdl-source/include -I/work/sdl-build/include'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c "$sound" "$sdl" -lm -ldl -lpthread -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c "$sound" "$sdl" -lm -ldl -lpthread -o /work/fuzzer
