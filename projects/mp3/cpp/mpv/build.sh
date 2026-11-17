#!/bin/sh
set -eu
# PARSARIUM_BUILD=coverage builds the replay/libFuzzer image; afl builds the AFL++ overlay.
# FFmpeg, libplacebo and mpv are configured exactly as in projects/mp3/c/mpv/build.sh:
# FFmpeg with mp3 as its only demuxer, libplacebo with every backend off, and a
# static libmpv. Only the call site differs (a C++17 translation unit instead of C).
mode=${PARSARIUM_BUILD:-coverage}
case "$mode" in
coverage)
  cc=clang cxx=clang++
  # One instrumentation set for FFmpeg, libplacebo, mpv and the harness, so
  # source coverage observes FFmpeg's ID3v2 reader and MP3 demuxer and mpv's
  # demux_lavf.c, not only the C++ call site.
  common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined -fno-sanitize=function'
  ;;
afl)
  # AFL++ instruments only FFmpeg's tagged-MP3 parsing sources and mpv's
  # libavformat demuxer wrapper: the ID3v2 and ID3v1 readers, the MP3 demuxer,
  # the ReplayGain tag export mp3dec.c calls, the MPEG audio header decoder and
  # frame parser it uses, and demux_lavf.c. The rest of libmpv, libavformat,
  # libavcodec, libplacebo and the C++ harness stay uninstrumented. Sanitizers stay on.
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
link="-Wl,--start-group $libs -Wl,--end-group $(pkg-config --libs libass) -lz -lm -ldl -lpthread"

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
cxxflags="-std=c++17 $common -I/work/source/include"
if [ "$mode" = coverage ]; then
  clang++ $cxxflags -c /work/harness.cpp -o /work/harness.o
  clang++ $cxxflags -c /work/replay.cpp -o /work/replay.o
  clang++ $cxxflags -c /work/fuzz.cpp -o /work/fuzz.o
  # Linked as in projects/mp3/c/mpv: replay without the libFuzzer runtime.
  clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping -fsanitize=address,undefined \
    /work/harness.o /work/replay.o $link -o /work/replay
  clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer,address,undefined \
    /work/harness.o /work/fuzz.o $link -o /work/fuzzer
else
  afl-clang-fast++ $cxxflags -c /work/harness.cpp -o /work/harness.o
  afl-clang-fast++ $cxxflags -c /work/replay.cpp -o /work/replay.o
  afl-clang-fast++ $cxxflags -fsanitize=fuzzer -c /work/fuzz.cpp -o /work/fuzz.o
  # The allowlist leaves the C++ harness objects without their own guards.
  for object in /work/harness.o /work/replay.o /work/fuzz.o; do
    if readelf -SW "$object" | grep -q __sancov_guards; then
      echo "$object carries its own AFL++ guards" >&2
      exit 1
    fi
  done
  afl-clang-fast++ $cxxflags /work/harness.o /work/replay.o $link -o /work/replay
  afl-clang-fast++ $cxxflags -fsanitize=fuzzer /work/harness.o /work/fuzz.o $link -o /work/fuzzer
fi
# Both binaries must carry libmpv's libavformat demuxer and FFmpeg's ID3v2
# reader and MP3 demuxer, and be linked from a C++ translation unit against the
# C++ runtime.
for binary in /work/replay /work/fuzzer; do
  llvm-nm "$binary" | grep -q ' T mpv_command$'
  llvm-nm "$binary" | grep -Eq ' [DR] demuxer_desc_lavf$'
  llvm-nm "$binary" | grep -Eq ' [DR] ff_mp3_demuxer$'
  llvm-nm "$binary" | grep -q ' T ff_id3v2_read_dict$'
  llvm-nm "$binary" | grep -q ' T _Z19parsarium_parse_mp3PKhmR20parsarium_mp3_result$'
  readelf -dW "$binary" | grep -q 'NEEDED.*libstdc++'
done
