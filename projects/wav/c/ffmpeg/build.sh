#!/bin/sh
set -eu
cd /work/source
./configure --cc=clang --disable-everything --disable-autodetect --disable-programs --disable-doc \
 --disable-network --disable-asm --disable-avdevice --disable-avfilter --disable-swscale \
 --disable-swresample --disable-shared --enable-static \
 --enable-protocol=file --enable-demuxer=mov,mp3,wav,image2,ppm_pipe \
 --enable-decoder=h264,aac,mp3,pcm_u8,pcm_s16le,pcm_s24le,pcm_s32le,pcm_f32le,pcm_f64le,ppm --enable-parser=h264,aac,mpegaudio \
 --extra-cflags='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 --extra-ldflags='-fprofile-instr-generate'
make -j 4 libavformat/libavformat.a libavcodec/libavcodec.a libavutil/libavutil.a
common='-O1 -g -fno-omit-frame-pointer -I/work/source'
libs='/work/source/libavformat/libavformat.a /work/source/libavcodec/libavcodec.a /work/source/libavutil/libavutil.a -lm -lz -lpthread'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c $libs -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c $libs -o /work/fuzzer
