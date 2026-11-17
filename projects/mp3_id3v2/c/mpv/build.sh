#!/bin/sh
set -eu
# PARSARIUM_BUILD=coverage builds the replay/libFuzzer image; afl builds the AFL++ overlay.
mode=${PARSARIUM_BUILD:-coverage}
case "$mode" in
coverage)
  cc=clang cxx=clang++
  # FFmpeg, libplacebo and mpv share one instrumentation set, so source
  # coverage and libFuzzer observe FFmpeg's ID3v2 reader and MP3 demuxer, not
  # only the libmpv wrapper.
  common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined -fno-sanitize=function'
  ;;
afl)
  # AFL++ instruments only FFmpeg's tagged-MP3 parsing sources and mpv's
  # libavformat demuxer wrapper: the ID3v2 and ID3v1 readers, the MP3 demuxer,
  # the ReplayGain tag export mp3dec.c calls, the MPEG audio header decoder and
  # frame parser it uses, and demux_lavf.c. The rest of libmpv, libavformat,
  # libavcodec, libplacebo and the C harness stay uninstrumented. Sanitizers stay on.
  printf '%s\n' \
    'src: id3v2.c' 'src: mp3dec.c' 'src: id3v1.c' \
    'src: replaygain.c' 'src: mpegaudiodecheader.c' \
    'src: mpegaudio_parser.c' 'src: *demux/demux_lavf.c' > /work/afl-allowlist.txt
  export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_QUIET=1
  cc=afl-clang-fast cxx=afl-clang-fast++
  common='-O1 -g -fno-omit-frame-pointer -fsanitize=address,undefined -fno-sanitize=function'
  ;;
*)
  echo "unknown PARSARIUM_BUILD: $mode" >&2
  exit 2
  ;;
esac
# Configure-time test programs run under the sanitizers; keep them quiet.
export ASAN_OPTIONS=detect_leaks=0 LLVM_PROFILE_FILE=/dev/null

# FFmpeg 9.0.2 from its pinned release tarball. mp3 is the only demuxer, so no
# other FFmpeg demuxer can claim the input; avformat_open_input reads the
# leading ID3v2 tag through libavformat/id3v2.c for it. Both MP3 decoders and
# the MPEG audio parser keep stream probing close to the catalog build. mpv
# requires libavfilter, libswresample and libswscale. Threads are off so
# FFmpeg decoding is single-threaded; zlib serves compressed ID3v2.4 frames.
cd /work/ffmpeg
./configure --prefix=/work/ffmpeg-install --cc="$cc" --cxx="$cxx" \
  --disable-everything --disable-autodetect --disable-programs --disable-doc \
  --disable-network --disable-asm --disable-pthreads --disable-avdevice \
  --disable-shared --enable-static --enable-zlib \
  --enable-protocol=file --enable-demuxer=mp3 \
  --enable-decoder=mp3float,mp3 --enable-parser=mpegaudio \
  --extra-cflags="$common" --extra-cxxflags="$common" --extra-ldflags="$common"
make -j 4
make install
ff=/work/ffmpeg-install/lib
test "$(llvm-nm $ff/libavformat.a | grep -Ec ' [DR] ff_[a-z0-9_]+_demuxer$')" = 1
llvm-nm $ff/libavformat.a | grep -Eq ' [DR] ff_mp3_demuxer$'
llvm-nm $ff/libavformat.a | grep -q ' T ff_id3v2_read_dict$'

# libplacebo 7.387.0, static, with every optional backend off. mpv links it
# for its renderer; the null video output used here does not call it.
cd /work
CC="$cc" CXX="$cxx" CFLAGS="$common" CXXFLAGS="$common" LDFLAGS="$common" \
  meson setup /work/libplacebo-build /work/libplacebo \
  --prefix=/work/deps --libdir=lib --buildtype=plain --default-library=static \
  --wrap-mode=nodownload --auto-features=disabled -Ddemos=false -Dtests=false
ninja -C /work/libplacebo-build
meson install -C /work/libplacebo-build

# libmpv 0.42.0 as a static library against the instrumented FFmpeg and
# libplacebo. Optional features are off; libass is Ubuntu's, as mpv requires it.
export PKG_CONFIG_PATH=/work/ffmpeg-install/lib/pkgconfig:/work/deps/lib/pkgconfig
CC="$cc" CXX="$cxx" CFLAGS="$common" CXXFLAGS="$common" LDFLAGS="$common" \
  meson setup /work/mpv-build /work/source \
  --buildtype=plain --default-library=static --wrap-mode=nodownload --auto-features=disabled \
  -Dlibmpv=true -Dcplayer=false -Dgpl=true -Dbuild-date=false -Dlua=disabled -Dgl=disabled \
  -Dtests=false -Dfuzzers=false
ninja -C /work/mpv-build
mpv=/work/mpv-build/libmpv.a
llvm-nm $mpv | grep -q ' T mpv_create$'
llvm-nm $mpv | grep -Eq ' [DR] demuxer_desc_lavf$'

libs="$mpv /work/deps/lib/libplacebo.a $ff/libavfilter.a $ff/libavformat.a $ff/libavcodec.a $ff/libswresample.a $ff/libswscale.a $ff/libavutil.a"
for archive in $libs; do test -f "$archive"; done
syslibs="$(pkg-config --libs libass) -lz -lm -ldl -lpthread"

# Archive members that carry AFL++ pcguard sections.
guarded() {
  readelf -SW "$1" | awk '/^File: /{member=$2} /__sancov_guards/{print member}' | sort -u
}
if [ "$mode" = afl ]; then
  guarded $ff/libavformat.a > /work/afl-guarded.txt
  guarded $ff/libavcodec.a >> /work/afl-guarded.txt
  guarded $mpv >> /work/afl-guarded.txt
  for member in 'libavformat\.a\(id3v2\.o\)' 'libavformat\.a\(mp3dec\.o\)' 'libavformat\.a\(id3v1\.o\)' \
      'libavformat\.a\(replaygain\.o\)' 'libavcodec\.a\(mpegaudiodecheader\.o\)' \
      'libavcodec\.a\(mpegaudio_parser\.o\)' 'libmpv\.a\(.*demux_lavf\.c\.o\)'; do
    grep -Eq "$member\$" /work/afl-guarded.txt
  done
  if grep -Ev 'libavformat\.a\((id3v2|mp3dec|id3v1|replaygain)\.o\)$|libavcodec\.a\((mpegaudiodecheader|mpegaudio_parser)\.o\)$|libmpv\.a\(.*demux_lavf\.c\.o\)$' /work/afl-guarded.txt; then
    echo "AFL++ guards outside the tagged-MP3 parser sources and demux_lavf.c" >&2
    exit 1
  fi
  for archive in /work/deps/lib/libplacebo.a $ff/libavfilter.a $ff/libswresample.a $ff/libswscale.a $ff/libavutil.a; do
    if [ -n "$(guarded "$archive")" ]; then
      echo "$archive carries AFL++ guards outside the tagged-MP3 parser sources" >&2
      exit 1
    fi
  done
fi

cd /work
if [ "$mode" = coverage ]; then
  clang $common -I/work/source/include -c /work/harness.c -o /work/harness.o
  clang $common -c /work/replay.c -o /work/replay.o
  clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping -fsanitize=address,undefined \
    /work/harness.o /work/replay.o -Wl,--start-group $libs -Wl,--end-group $syslibs -o /work/replay
  clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer,address,undefined \
    /work/harness.o -Wl,--start-group $libs -Wl,--end-group $syslibs -o /work/fuzzer
else
  afl-clang-fast $common -I/work/source/include -c /work/harness.c -o /work/harness.o
  afl-clang-fast $common -c /work/replay.c -o /work/replay.o
  # The allowlist leaves the C harness objects without their own guards.
  for object in /work/harness.o /work/replay.o; do
    if readelf -SW "$object" | grep -q __sancov_guards; then
      echo "$object carries its own AFL++ guards" >&2
      exit 1
    fi
  done
  afl-clang-fast++ $common /work/harness.o /work/replay.o \
    -Wl,--start-group $libs -Wl,--end-group $syslibs -o /work/replay
  afl-clang-fast++ $common -fsanitize=fuzzer /work/harness.o \
    -Wl,--start-group $libs -Wl,--end-group $syslibs -o /work/fuzzer
fi
# Both binaries must carry libmpv's libavformat demuxer and FFmpeg's ID3v2
# reader and MP3 demuxer.
for binary in /work/replay /work/fuzzer; do
  llvm-nm "$binary" | grep -q ' T mpv_command$'
  llvm-nm "$binary" | grep -Eq ' [DR] demuxer_desc_lavf$'
  llvm-nm "$binary" | grep -Eq ' [DR] ff_mp3_demuxer$'
  llvm-nm "$binary" | grep -q ' T ff_id3v2_read_dict$'
done
