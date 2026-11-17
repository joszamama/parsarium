#!/bin/sh
set -eu
src=/work/libheif-1.23.7
common='-O1 -g -fno-omit-frame-pointer'
cov='-fprofile-instr-generate -fcoverage-mapping'
fuzz='-fsanitize=fuzzer-no-link,address,undefined'
# Static libheif with every codec, plugin, and tool off: only the native ISO BMFF
# box, item, and sequence-track parser is built. Decoding is not needed for
# heif_context_read_from_file or track resolution.
opts='-DBUILD_SHARED_LIBS=OFF -DENABLE_PLUGIN_LOADING=OFF -DBUILD_TESTING=OFF -DBUILD_DOCUMENTATION=OFF
 -DWITH_EXAMPLES=OFF -DWITH_GDK_PIXBUF=OFF -DWITH_LIBSHARPYUV=OFF -DWITH_HEADER_COMPRESSION=OFF
 -DWITH_LIBDE265=OFF -DWITH_X265=OFF -DWITH_X264=OFF -DWITH_OpenH264_DECODER=OFF -DWITH_AOM_DECODER=OFF
 -DWITH_AOM_ENCODER=OFF -DWITH_DAV1D=OFF -DWITH_SvtEnc=OFF -DWITH_RAV1E=OFF -DWITH_JPEG_DECODER=OFF
 -DWITH_JPEG_ENCODER=OFF -DWITH_OpenJPEG_ENCODER=OFF -DWITH_OpenJPEG_DECODER=OFF -DWITH_FFMPEG_DECODER=OFF
 -DWITH_OPENJPH_ENCODER=OFF -DWITH_UNCOMPRESSED_CODEC=OFF'
libheif() {
 cmake -S "$src" -B "$1" -DCMAKE_BUILD_TYPE= -DCMAKE_INSTALL_PREFIX="$1/install" -DCMAKE_INSTALL_LIBDIR=lib \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common $2" -DCMAKE_CXX_FLAGS="$common $2" $opts
 cmake --build "$1" --target heif -j 4
 cmake --install "$1"
}
libheif /work/coverage-build "$cov"
inc='-I/work/coverage-build/install/include'
clang -std=c11 $common $cov $inc -c /work/harness.c -o /work/harness.o
clang -std=c11 $common $cov $inc -c /work/replay.c -o /work/replay.o
clang++ $common $cov /work/harness.o /work/replay.o /work/coverage-build/install/lib/libheif.a -lpthread -lm -o /work/replay
libheif /work/fuzz-build "$fuzz"
inc='-I/work/fuzz-build/install/include'
clang -std=c11 $common $fuzz $inc -c /work/harness.c -o /work/harness-fuzz.o
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness-fuzz.o /work/fuzz-build/install/lib/libheif.a -lpthread -lm -o /work/fuzzer
