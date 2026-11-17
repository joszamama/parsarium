#!/bin/sh
set -eu
mode=${PARSARIUM_BUILD:-coverage}
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
case "$mode" in
coverage)
  ff_cc=clang
  ff_flags='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
  link_flags='-fprofile-instr-generate'
  mlt_flags="$ff_flags"
  ;;
afl)
  ff_cc=afl-clang-fast
  ff_flags='-O1 -g -fno-omit-frame-pointer'
  link_flags=''
  mlt_flags='-O1 -g -fno-omit-frame-pointer'
  # mov.c contains the FFmpeg MOV/MP4 syntax and box parser. MLT, the C
  # adapter, and every other FFmpeg translation unit are excluded from AFL.
  printf 'src:mov.c\n' > /work/afl-allowlist.txt
  export AFL_LLVM_INSTRUMENT=CLASSIC AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  ;;
*) echo "unknown PARSARIUM_BUILD: $mode" >&2; exit 2 ;;
esac
cd /work/ffmpeg
./configure --prefix=/work/install --libdir=/work/install/lib \
  --cc="$ff_cc" --ld="$ff_cc" --disable-everything --disable-autodetect \
  --disable-programs --disable-doc --disable-network --disable-asm \
  --disable-avdevice --enable-shared --disable-static --enable-pic \
  --enable-avfilter --enable-swscale --enable-swresample \
  --enable-protocol=file --enable-demuxer=mov \
  --enable-decoder=h264,aac --enable-parser=h264,aac \
  --extra-cflags="$ff_flags" --extra-ldflags="$link_flags"
make -j 4
make install
test "$(pkg-config --modversion libavformat)" = 63.1.102
if [ "$mode" = coverage ]; then
  readelf -SW /work/install/lib/libavformat.so.63 | grep -q __llvm_covmap
fi
cd /work
# Build only MLT's framework, core module, and avformat producer. Every other
# optional module is disabled to keep dependencies and parser scope explicit.
modules='DECKLINK FREI0R GDK GLAXNIMATE_QT6 JACKRACK KDENLIVE MOVIT NDI NORMALIZE OLDFILM OPENCV OPENFX PLACEBO PLUS PLUSGPL QT6 RESAMPLE RTAUDIO RUBBERBAND RNNOISE SDL1 SDL2 SOX SPATIALAUDIO VIDSTAB VORBIS XINE XML'
options=''
for module in $modules; do options="$options -DMOD_${module}=OFF"; done
cmake -S /work/mlt -B /work/mlt-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/work/install \
  -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$mlt_flags" -DCMAKE_CXX_FLAGS="$mlt_flags" \
  -DCMAKE_SHARED_LINKER_FLAGS="$link_flags" -DCMAKE_MODULE_LINKER_FLAGS="$link_flags" \
  -DCMAKE_PREFIX_PATH=/work/install -DGPL=OFF -DGPL3=OFF -DUSE_AVDEVICE=OFF \
  -DMOD_AVFORMAT=ON -DBUILD_TESTING=OFF -DBUILD_DOCS=OFF $options
cmake --build /work/mlt-build -j 4
cmake --install /work/mlt-build
test -f /work/install/lib/mlt-7/libmltavformat.so
test -f /work/install/lib/libmlt-7.so
if [ "$mode" = coverage ]; then
  readelf -SW /work/install/lib/mlt-7/libmltavformat.so | grep -q __llvm_covmap
fi
