#!/bin/sh
set -eu
mode=${PARSARIUM_BUILD:-coverage}
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig FFMPEGDIR=/work/install
base_flags='-O1 -g -fno-omit-frame-pointer'
case "$mode" in
coverage)
  ff_cc=clang
  os_cc=clang os_cxx=clang++
  ff_flags="$base_flags -fprofile-instr-generate -fcoverage-mapping"
  os_flags="$ff_flags"
  link_flags='-fprofile-instr-generate'
  ;;
afl)
  ff_cc=afl-clang-fast
  os_cc=afl-clang-fast os_cxx=afl-clang-fast++
  ff_flags="$base_flags"
  os_flags="$base_flags"
  link_flags=''
  # Feedback is limited to the FFmpeg MOV/MP4 box parser and libopenshot's
  # FFmpegReader. OpenShotAudio, the rest of libopenshot and FFmpeg, Qt, and
  # the C++ harness carry no AFL edges.
  printf 'src:mov.c\nsrc:FFmpegReader.cpp\n' > /work/afl-allowlist.txt
  export AFL_LLVM_INSTRUMENT=CLASSIC AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  ;;
*) echo "unknown PARSARIUM_BUILD: $mode" >&2; exit 2 ;;
esac

# FFmpeg 9.0.2: only the file protocol, MOV/MP4 demuxer, and the H.264/AAC
# decoders the control needs. libopenshot requires avdevice and swscale, and
# uses swresample for audio, so those libraries are built without devices.
cd /work/ffmpeg
./configure --prefix=/work/install --libdir=/work/install/lib \
  --cc="$ff_cc" --ld="$ff_cc" --disable-everything --disable-autodetect \
  --disable-programs --disable-doc --disable-network --disable-asm \
  --enable-shared --disable-static --enable-pic \
  --enable-avdevice --disable-avfilter --enable-swscale --enable-swresample \
  --enable-protocol=file --enable-demuxer=mov \
  --enable-decoder=h264,aac --enable-parser=h264,aac \
  --extra-cflags="$ff_flags" --extra-ldflags="$link_flags"
make -j 4
make install
test "$(pkg-config --modversion libavformat)" = 63.1.102
if [ "$mode" = coverage ]; then
  readelf -SW /work/install/lib/libavformat.so.63 | grep -q __llvm_covmap
fi

# libopenshot-audio 1.0.2 (JUCE): never instrumented. Release with NDEBUG and
# the same optimisation level as libopenshot so JUCE headers agree.
cmake -S /work/libopenshot-audio -B /work/libopenshot-audio-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/work/install \
  -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$base_flags" -DCMAKE_CXX_FLAGS="$base_flags" \
  -DCMAKE_C_FLAGS_RELEASE=-DNDEBUG -DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
  -DENABLE_AUDIO_DOCS=OFF -DAUTO_INSTALL_DOCS=OFF
cmake --build /work/libopenshot-audio-build -j 4
cmake --install /work/libopenshot-audio-build
test -f /work/install/lib/cmake/OpenShotAudio/OpenShotAudioConfig.cmake

# libopenshot 1.1.1: Qt 6, OpenMP, bundled JsonCpp, and the FFmpeg above.
# ImageMagick, OpenCV, Wayland capture, bindings, docs, and tests are off so
# FFmpegReader is the only media reader on the path.
cmake -S /work/libopenshot -B /work/libopenshot-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/work/install \
  -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_C_COMPILER="$os_cc" -DCMAKE_CXX_COMPILER="$os_cxx" \
  -DCMAKE_C_FLAGS="$os_flags" -DCMAKE_CXX_FLAGS="$os_flags" \
  -DCMAKE_C_FLAGS_RELEASE=-DNDEBUG -DCMAKE_CXX_FLAGS_RELEASE=-DNDEBUG \
  -DCMAKE_SHARED_LINKER_FLAGS="$link_flags" -DCMAKE_EXE_LINKER_FLAGS="$link_flags" \
  -DCMAKE_PREFIX_PATH=/work/install -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DUSE_QT6=ON -DENABLE_MAGICK=OFF -DENABLE_OPENCV=OFF -DENABLE_WAYLAND_CAPTURE=OFF \
  -DUSE_SYSTEM_JSONCPP=OFF -DENABLE_PYTHON=OFF -DENABLE_RUBY=OFF -DENABLE_JAVA=OFF \
  -DENABLE_LIB_DOCS=OFF -DBUILD_TESTING=OFF
cmake --build /work/libopenshot-build --target openshot -j 4
cmake --install /work/libopenshot-build
test -f /work/install/lib/libopenshot.so
test -f /work/libopenshot-build/compile_commands.json
# The reader must resolve the source-built FFmpeg, never a system copy.
LD_LIBRARY_PATH=/work/install/lib ldd /work/install/lib/libopenshot.so \
  | grep -q '/work/install/lib/libavformat.so.63'
if [ "$mode" = coverage ]; then
  readelf -SW /work/install/lib/libopenshot.so | grep -q __llvm_covmap
fi
