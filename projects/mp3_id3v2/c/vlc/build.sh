#!/bin/sh
set -eu
# TagLib and VLC are both built here, not in a separate source step, so the
# AFL++ overlay's compiler rewrite instruments TagLib's ID3v2 parser, VLC's
# own ID3v2 reader, the MPEG audio demuxer and packetizer, and the harness.
cov='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'

# TagLib 1.13.1 with the two patches VLC 3.0.24 applies in
# contrib/src/taglib/rules.mak. The patches come from the pinned VLC archive;
# the ID3v2 readStyle patch defines VLC_PATCHED_TAGLIB_ID3V2_READSTYLE, which
# modules/meta_engine/taglib.cpp checks. Bindings off as in VLC's contrib.
cd /work/taglib-1.13.1
patch -p1 < /work/source/contrib/src/taglib/0001-Implement-ID3v2-readStyle-avoid-worst-case.patch
patch -p1 < /work/source/contrib/src/taglib/0001-Fix-crash-with-invalid-WAV-files-1163-1164.patch
grep -q VLC_PATCHED_TAGLIB_ID3V2_READSTYLE taglib/toolkit/taglib.h
cmake -S /work/taglib-1.13.1 -B /work/taglib-build -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$cov" -DCMAKE_CXX_FLAGS="$cov" \
  -DCMAKE_INSTALL_PREFIX=/work/taglib-install -DCMAKE_INSTALL_LIBDIR=lib \
  -DBUILD_SHARED_LIBS=OFF -DBUILD_BINDINGS=OFF -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF
cmake --build /work/taglib-build -j 6
cmake --install /work/taglib-build

# With shared libraries off, VLC disables dynamic plugins and its module bank
# registers the plugins named in the harness's vlc_static_modules table; this
# is the static mode upstream uses for its own demux fuzzers.
cd /work/source
PKG_CONFIG_PATH=/work/taglib-install/lib/pkgconfig ./configure CC=clang CXX=clang++ BUILDCC=clang \
  CFLAGS="$cov" CXXFLAGS="$cov" LDFLAGS='-fprofile-instr-generate' \
  --disable-shared --enable-static --disable-vlc --disable-nls --disable-update-check \
  --disable-lua --disable-sout --disable-vlm --disable-libgcrypt --disable-gnutls --disable-dbus \
  --disable-mad --disable-a52 --disable-faad --disable-vpx --disable-x264 --disable-avcodec \
  --disable-avformat --disable-swscale --disable-postproc --disable-libva --disable-vdpau \
  --disable-qt --disable-skins2 --disable-ncurses --disable-xcb --disable-xvideo --disable-wayland \
  --disable-freetype --disable-alsa --disable-pulse --disable-jack --disable-sndio --disable-v4l2 \
  --disable-live555 --disable-chromecast --disable-chromaprint --disable-libplacebo --enable-taglib
# configure only warns when TagLib is missing; require the pinned one.
grep -q '^LTLIBtaglib = libtaglib_plugin.la' modules/Makefile
grep -q '^TAGLIB_CFLAGS = .*/work/taglib-install/include' modules/Makefile
# Only the core, the libVLC API and the five plugins the harness registers.
make -C compat -j 6
make -C src -j 6
make -C lib -j 6
plugins='filesystem skiptags es packetizer_mpegaudio taglib'
make -C modules -j 6 $(for p in $plugins; do printf 'lib%s_plugin.la ' "$p"; done)
deps() { sed -n "s/^dependency_libs='\(.*\)'$/\1/p" "$1" | tr ' ' '\n' | grep -v '\.la$' | tr '\n' ' '; }
archives=''
plugin_deps=''
for p in $plugins; do
  archives="$archives /work/source/modules/.libs/lib${p}_plugin.a"
  plugin_deps="$plugin_deps $(deps modules/lib${p}_plugin.la)"
done
vlc_libs="-Wl,--start-group $archives \
 /work/source/lib/.libs/libvlc.a /work/source/src/.libs/libvlccore.a /work/source/compat/.libs/libcompat.a -Wl,--end-group \
 $(deps src/libvlccore.la) $plugin_deps /work/taglib-install/lib/libtag.a -lz -lstdc++ -lpthread -ldl -lm"
cd /work
common='-O1 -g -fno-omit-frame-pointer -I/work/source/include'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c $vlc_libs -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -fprofile-instr-generate /work/harness.c $vlc_libs -o /work/fuzzer
# Both binaries must carry the statically registered plugins, not stubs, and
# TagLib's ID3v2 tag parser.
for binary in /work/replay /work/fuzzer; do
  for p in $plugins; do
    symbol=$p
    [ "$p" = packetizer_mpegaudio ] && symbol=mpegaudio
    llvm-nm "$binary" | grep -q " T vlc_entry__${symbol}$"
  done
  llvm-nm "$binary" | grep -Eq ' [DR] vlc_static_modules$'
  llvm-nm -C "$binary" | grep -q ' T TagLib::ID3v2::Tag::parse(TagLib::ByteVector const&)$'
done
