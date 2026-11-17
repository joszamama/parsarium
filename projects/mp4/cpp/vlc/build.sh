#!/bin/sh
set -eu
# PARSARIUM_BUILD=coverage builds the replay/libFuzzer image; afl builds the AFL++ overlay.
# The VLC build is the same as projects/mp4/c/vlc/build.sh: static libvlccore and libVLC,
# dynamic plugins off, and only the file access and MP4 demuxer plugins built. Only the
# call site differs (a C++17 translation unit instead of C).
mode=${PARSARIUM_BUILD:-coverage}
common='-O1 -g -fno-omit-frame-pointer'
case "$mode" in
coverage)
  cc=clang cxx=clang++
  vlc_flags="$common -fprofile-instr-generate -fcoverage-mapping"
  vlc_ldflags='-fprofile-instr-generate'
  ;;
afl)
  # AFL++ instruments only VLC's MP4 demuxer plugin sources, so every feedback
  # tuple comes from that plugin: not libvlccore, file access, or the C++ harness.
  printf 'src: *demux/mp4/*\nsrc: *demux/asf/asfpacket.c\n' > /work/afl-allowlist.txt
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_QUIET=1
  cc=afl-clang-fast cxx=afl-clang-fast++
  vlc_flags="$common"
  vlc_ldflags=''
  ;;
*)
  echo "unknown PARSARIUM_BUILD: $mode" >&2
  exit 2
  ;;
esac
cd /work/source
./configure CC="$cc" CXX="$cxx" BUILDCC=clang CFLAGS="$vlc_flags" CXXFLAGS="$vlc_flags" LDFLAGS="$vlc_ldflags" \
  --disable-shared --enable-static --disable-vlc --disable-nls --disable-update-check \
  --disable-lua --disable-sout --disable-vlm --disable-libgcrypt --disable-gnutls --disable-dbus \
  --disable-mad --disable-a52 --disable-faad --disable-vpx --disable-x264 --disable-avcodec \
  --disable-avformat --disable-swscale --disable-postproc --disable-libva --disable-vdpau \
  --disable-qt --disable-skins2 --disable-ncurses --disable-xcb --disable-xvideo --disable-wayland \
  --disable-freetype --disable-alsa --disable-pulse --disable-jack --disable-sndio --disable-v4l2 \
  --disable-live555 --disable-chromecast --disable-chromaprint --disable-libplacebo --disable-taglib
# Only the core, the libVLC API, file access, and the MP4 demuxer are built.
make -C compat -j 6
make -C src -j 6
make -C lib -j 6
make -C modules -j 6 libfilesystem_plugin.la libmp4_plugin.la
if [ "$mode" = afl ]; then
  readelf -SW modules/.libs/libmp4_plugin.a | grep -q __sancov_guards
  for archive in compat/.libs/libcompat.a src/.libs/libvlccore.a lib/.libs/libvlc.a modules/.libs/libfilesystem_plugin.a; do
    if readelf -SW "$archive" | grep -q __sancov_guards; then
      echo "$archive carries AFL++ guards outside the MP4 demuxer" >&2
      exit 1
    fi
  done
fi
deps() { sed -n "s/^dependency_libs='\(.*\)'$/\1/p" "$1" | tr ' ' '\n' | grep -v '\.la$' | tr '\n' ' '; }
vlc_libs="-Wl,--start-group /work/source/modules/.libs/libfilesystem_plugin.a /work/source/modules/.libs/libmp4_plugin.a \
 /work/source/lib/.libs/libvlc.a /work/source/src/.libs/libvlccore.a /work/source/compat/.libs/libcompat.a -Wl,--end-group \
 $(deps src/libvlccore.la) $(deps modules/libmp4_plugin.la) -lpthread -ldl -lm"
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
# Both binaries must carry the statically registered demuxer, not a stub, and be
# linked from a C++ translation unit against the C++ runtime.
for binary in /work/replay /work/fuzzer; do
  llvm-nm "$binary" | grep -q ' T vlc_entry__mp4$'
  llvm-nm "$binary" | grep -Eq ' [DR] vlc_static_modules$'
  llvm-nm "$binary" | grep -q ' T _Z19parsarium_parse_mp4PKhmR20parsarium_mp4_result$'
  readelf -dW "$binary" | grep -q 'NEEDED.*libstdc++'
done
