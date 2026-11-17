#!/bin/sh
set -eu
# PARSARIUM_BUILD=coverage builds the replay/libFuzzer image; afl builds the AFL++ overlay.
# TagLib 1.13.1 (VLC 3.0.24's contrib pin, with VLC's two contrib patches applied in the
# Dockerfile) is built as a static library first. VLC is configured like
# projects/mp4/cpp/vlc (static libvlccore and libVLC, dynamic plugins off) but with the
# TagLib meta reader enabled against that build. Only the five plugins on the local MP3
# preparse path are built.
mode=${PARSARIUM_BUILD:-coverage}
common='-O1 -g -fno-omit-frame-pointer'
case "$mode" in
coverage)
  cc=clang cxx=clang++
  flags="$common -fprofile-instr-generate -fcoverage-mapping"
  ldflags='-fprofile-instr-generate'
  ;;
afl)
  # AFL++ instruments only the MP3 and ID3v2 parsers on the preparse path: TagLib,
  # VLC's native ID3 headers, the tag-skipping stream filter,
  # the MPEG audio ES demuxer and its packetizer. libvlccore, libVLC, file access and
  # the C++ harness carry no guards.
  printf '%s\n' 'src: */taglib-1.13.1/taglib/*' \
    'src: *meta_engine/*' 'src: *stream_filter/*' 'src: *demux/mpeg/*' \
    'src: *packetizer/*' > /work/afl-allowlist.txt
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_QUIET=1
  cc=afl-clang-fast cxx=afl-clang-fast++
  flags="$common"
  ldflags=''
  ;;
*)
  echo "unknown PARSARIUM_BUILD: $mode" >&2
  exit 2
  ;;
esac
cmake -S /work/taglib-1.13.1 -B /work/taglib-build -DCMAKE_BUILD_TYPE=None \
  -DCMAKE_C_COMPILER="$cc" -DCMAKE_CXX_COMPILER="$cxx" -DCMAKE_C_FLAGS="$flags" -DCMAKE_CXX_FLAGS="$flags" \
  -DBUILD_SHARED_LIBS=OFF -DBUILD_BINDINGS=OFF -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_INSTALL_PREFIX=/work/taglib-install -DCMAKE_INSTALL_LIBDIR=lib
cmake --build /work/taglib-build -j 6
cmake --install /work/taglib-build
export PKG_CONFIG_PATH=/work/taglib-install/lib/pkgconfig
test "$(pkg-config --modversion taglib)" = 1.13.1
# The readStyle patch defines this marker; VLC's meta reader changes its IOStream path on it.
grep -q VLC_PATCHED_TAGLIB_ID3V2_READSTYLE /work/taglib-install/include/taglib/taglib.h
cd /work/source
./configure CC="$cc" CXX="$cxx" BUILDCC=clang CFLAGS="$flags" CXXFLAGS="$flags" LDFLAGS="$ldflags" \
  --disable-shared --enable-static --disable-vlc --disable-nls --disable-update-check \
  --disable-lua --disable-sout --disable-vlm --disable-libgcrypt --disable-gnutls --disable-dbus \
  --disable-mad --disable-a52 --disable-faad --disable-vpx --disable-x264 --disable-avcodec \
  --disable-avformat --disable-swscale --disable-postproc --disable-libva --disable-vdpau \
  --disable-qt --disable-skins2 --disable-ncurses --disable-xcb --disable-xvideo --disable-wayland \
  --disable-freetype --disable-alsa --disable-pulse --disable-jack --disable-sndio --disable-v4l2 \
  --disable-live555 --disable-chromecast --disable-chromaprint --disable-libplacebo --enable-taglib
# configure only warns when TagLib is missing; require the pinned build.
grep -q '^TAGLIB_LIBS = .*-L/work/taglib-install/lib -ltag' modules/Makefile
make -C compat -j 6
make -C src -j 6
make -C lib -j 6
make -C modules -j 6 libfilesystem_plugin.la libskiptags_plugin.la libes_plugin.la \
  libpacketizer_mpegaudio_plugin.la libtaglib_plugin.la
parsers='/work/taglib-install/lib/libtag.a modules/.libs/libskiptags_plugin.a
 modules/.libs/libes_plugin.a modules/.libs/libpacketizer_mpegaudio_plugin.a'
if [ "$mode" = afl ]; then
  for archive in $parsers; do
    if ! readelf -SW "$archive" | grep -q __sancov_guards; then
      echo "$archive carries no AFL++ guards" >&2
      exit 1
    fi
  done
  for archive in compat/.libs/libcompat.a src/.libs/libvlccore.a lib/.libs/libvlc.a modules/.libs/libfilesystem_plugin.a; do
    if readelf -SW "$archive" | grep -q __sancov_guards; then
      echo "$archive carries AFL++ guards outside the MP3 and ID3v2 parsers" >&2
      exit 1
    fi
  done
fi
deps() { sed -n "s/^dependency_libs='\(.*\)'$/\1/p" "$1" | tr ' ' '\n' | grep -v '\.la$' | tr '\n' ' '; }
vlc_libs="-Wl,--start-group /work/source/modules/.libs/libfilesystem_plugin.a /work/source/modules/.libs/libskiptags_plugin.a \
 /work/source/modules/.libs/libes_plugin.a /work/source/modules/.libs/libpacketizer_mpegaudio_plugin.a \
 /work/source/modules/.libs/libtaglib_plugin.a /work/source/lib/.libs/libvlc.a /work/source/src/.libs/libvlccore.a \
 /work/source/compat/.libs/libcompat.a -Wl,--end-group \
 $(deps src/libvlccore.la) $(deps modules/libes_plugin.la) $(deps modules/libtaglib_plugin.la) -lpthread -ldl -lm"
cd /work
cxxflags="-std=c++17 $common -I/work/source/include"
fuzz='-fsanitize=fuzzer,address,undefined'
if [ "$mode" = coverage ]; then
  clang++ $cxxflags -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp $vlc_libs -o /work/replay
  clang++ $cxxflags $fuzz -fprofile-instr-generate /work/harness.cpp /work/fuzz.cpp $vlc_libs -o /work/fuzzer
else
  fuzz="$fuzz -fno-sanitize=function"
  afl-clang-fast++ $cxxflags -c /work/harness.cpp -o /work/harness-replay.o
  afl-clang-fast++ $cxxflags -c /work/replay.cpp -o /work/replay.o
  afl-clang-fast++ $cxxflags $fuzz -c /work/harness.cpp -o /work/harness-fuzz.o
  afl-clang-fast++ $cxxflags $fuzz -c /work/fuzz.cpp -o /work/fuzz.o
  # The allowlist leaves the C++ harness objects without their own guards.
  for object in /work/harness-replay.o /work/replay.o /work/harness-fuzz.o /work/fuzz.o; do
    if readelf -SW "$object" | grep -q __sancov_guards; then
      echo "$object carries its own AFL++ guards" >&2
      exit 1
    fi
  done
  afl-clang-fast++ /work/harness-replay.o /work/replay.o $vlc_libs -o /work/replay
  afl-clang-fast++ $fuzz /work/harness-fuzz.o /work/fuzz.o $vlc_libs -o /work/fuzzer
fi
# Both binaries must carry the five statically registered plugins and TagLib's ID3v2
# parser, and be linked from a C++ translation unit against the C++ runtime.
for binary in /work/replay /work/fuzzer; do
  for plugin in filesystem skiptags es packetizer_mpegaudio taglib; do
    symbol=$plugin
    [ "$plugin" = packetizer_mpegaudio ] && symbol=mpegaudio
    llvm-nm "$binary" | grep -q " T vlc_entry__$symbol\$"
  done
  llvm-nm "$binary" | grep -Eq ' [DR] vlc_static_modules$'
  llvm-nm "$binary" | grep -q ' T _ZN6TagLib5ID3v23Tag'
  llvm-nm "$binary" | grep -q ' T _Z19parsarium_parse_mp3PKhmR20parsarium_mp3_result$'
  readelf -dW "$binary" | grep -q 'NEEDED.*libstdc++'
done
