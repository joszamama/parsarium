#!/bin/sh
set -eu
# VLC is built in build.sh, not a separate source step, so the AFL++ overlay's
# compiler rewrite instruments libvlccore and the MP4 demuxer as well as the
# harness. With shared libraries off, VLC disables dynamic plugins and its
# module bank registers the plugins named in the harness's vlc_static_modules
# table; this is the static mode upstream uses for its own demux fuzzers.
cd /work/source
./configure CC=clang CXX=clang++ BUILDCC=clang \
  CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
  CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
  LDFLAGS='-fprofile-instr-generate' \
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
deps() { sed -n "s/^dependency_libs='\(.*\)'$/\1/p" "$1" | tr ' ' '\n' | grep -v '\.la$' | tr '\n' ' '; }
vlc_libs="-Wl,--start-group /work/source/modules/.libs/libfilesystem_plugin.a /work/source/modules/.libs/libmp4_plugin.a \
 /work/source/lib/.libs/libvlc.a /work/source/src/.libs/libvlccore.a /work/source/compat/.libs/libcompat.a -Wl,--end-group \
 $(deps src/libvlccore.la) $(deps modules/libmp4_plugin.la) -lpthread -ldl -lm"
cd /work
common='-O1 -g -fno-omit-frame-pointer -I/work/source/include'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c $vlc_libs -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -fprofile-instr-generate /work/harness.c $vlc_libs -o /work/fuzzer
# Both binaries must carry the statically registered demuxer, not a stub.
for binary in /work/replay /work/fuzzer; do
  llvm-nm "$binary" | grep -q ' T vlc_entry__mp4$'
  llvm-nm "$binary" | grep -Eq ' [DR] vlc_static_modules$'
done
