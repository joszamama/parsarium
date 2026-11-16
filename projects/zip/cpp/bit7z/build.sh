#!/bin/sh
set -eu

# Build two parser libraries from the pinned sources, twice each: once with
# LLVM source coverage for the replay binary, and once with libFuzzer-compatible
# sanitizer instrumentation for the fuzzer.
#   - SevenZip 26.04: the upstream Format7zF bundle, i.e. the 7z.so shared
#     library that bit7z loads. No console or GUI program is built. Assembly is
#     not enabled, so every decoder is compiled from C/C++ with instrumentation.
#   - bit7z 4.1.0: the static wrapper library, compiled against the same pinned
#     SevenZip headers through BIT7Z_CUSTOM_7ZIP_PATH.
# Both harness binaries link 7z.so as a DT_NEEDED dependency so its counters
# and coverage are registered at process start.
cc=clang
cxx=clang++
jobs=${PARSARIUM_JOBS:-4}
base='-O1 -g -fno-omit-frame-pointer -DNDEBUG'
coverage='-fprofile-instr-generate -fcoverage-mapping'
# SevenZip's ZIP reader performs unaligned integer loads on the valid control
# on arm64. Preserve other UBSan checks and ASan while excluding alignment.
fuzz='-fsanitize=fuzzer-no-link,address,undefined -fno-sanitize=alignment'

build_sevenzip() {
  # Command-line variables override the makefile defaults: no -Werror, no
  # strip, and the instrumentation flags reach every compile and the link.
  make -C /work/sevenzip/CPP/7zip/Bundles/Format7zF -f makefile.gcc -j "$jobs" \
    O="$1" CC=$cc CXX=$cxx CFLAGS_WARN_WALL= CFLAGS_WARN= LFLAGS_STRIP= \
    CFLAGS_DEBUG=-DNDEBUG CFLAGS_BASE2="$base $2" CXXFLAGS_BASE2="$base $2" \
    LDFLAGS_STATIC_3="$2"
  mkdir -p "$3"
  cp "$1/7z.so" "$3/7z.so"
}
build_sevenzip /work/build-cov/7z "$coverage" /work/lib-cov
build_sevenzip /work/build-fuzz/7z "$fuzz" /work/lib-fuzz

configure_bit7z() {
  cmake -S /work/bit7z -B "$1" -G 'Unix Makefiles' \
    -DCMAKE_BUILD_TYPE=None -DCMAKE_C_COMPILER=$cc -DCMAKE_CXX_COMPILER=$cxx \
    -DCMAKE_C_FLAGS="$base $2" -DCMAKE_CXX_FLAGS="$base $2" \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCPM_SOURCE_CACHE=/work/cpm-cache \
    -DBIT7Z_CUSTOM_7ZIP_PATH=/work/sevenzip -DBIT7Z_AUTO_FORMAT=OFF \
    -DBIT7Z_BUILD_TESTS=OFF -DBIT7Z_BUILD_DOCS=OFF -DBIT7Z_USE_PCH=OFF \
    -DBIT7Z_DISABLE_USE_STD_FILESYSTEM=OFF
  # cmake/OutputOptions.cmake forces the archive into the source tree
  # (/work/bit7z/lib/<arch>/), shared by both builds, so move each one out
  # before the next build overwrites it.
  rm -f /work/bit7z/lib/*/libbit7z64.a
  cmake --build "$1" --target bit7z -j "$jobs"
  mkdir -p "$3"
  mv /work/bit7z/lib/*/libbit7z64.a "$3/libbit7z.a"
}
configure_bit7z /work/build-cov/bit7z "$coverage" /work/lib-cov
configure_bit7z /work/build-fuzz/bit7z "$fuzz" /work/lib-fuzz

# Every bit7z translation unit must carry the requested flags and be built
# against the pinned SevenZip headers. The key SevenZip ZIP reader, Deflate
# decoder and DLL export objects must carry the instrumentation sections.
python3 - <<'PY'
import json
import subprocess
from pathlib import Path

for build, flag in (("/work/build-cov", "-fcoverage-mapping"),
                    ("/work/build-fuzz", "-fsanitize=fuzzer-no-link,address,undefined")):
    entries = json.load(open(f"{build}/bit7z/compile_commands.json"))
    sources = {e["file"]: e.get("command") or " ".join(e["arguments"]) for e in entries}
    expected = {str(p) for p in Path("/work/bit7z/src").rglob("*.cpp")}
    if set(sources) != expected:
        raise SystemExit(f"unexpected bit7z sources in {build}: {sorted(set(sources) ^ expected)}")
    for path, text in sources.items():
        if flag not in text or "/work/sevenzip/CPP" not in text:
            raise SystemExit(f"uninstrumented or wrong SevenZip headers in {build}: {path}")

objects = ("ZipHandler.o", "ZipIn.o", "ZipItem.o", "ZipRegister.o", "DeflateDecoder.o",
           "CopyCoder.o", "ArchiveExports.o", "DllExports2.o", "CodecExports.o")
for build, section in (("/work/build-cov/7z", "__llvm_covfun"),
                       ("/work/build-fuzz/7z", "__sancov_cntrs")):
    for name in objects:
        path = f"{build}/{name}"
        listing = subprocess.run(["llvm-readelf", "--section-headers", path],
                                 check=True, capture_output=True, text=True).stdout
        symbols = subprocess.run(["llvm-nm", path], check=True,
                                 capture_output=True, text=True).stdout
        # The AFL++ overlay replaces Clang's sanitizer guards with AFL's own
        # counters. Both are real parser feedback, with different signatures.
        if section not in listing and not (section == "__sancov_cntrs" and "__afl_area_ptr" in symbols):
            raise SystemExit(f"uninstrumented SevenZip object in {build}: {name}")
PY

# Each archive must define the wrapper entry points the harness uses and
# carry only its own build's instrumentation.
bit7z_cov=/work/lib-cov/libbit7z.a
bit7z_fuzz=/work/lib-fuzz/libbit7z.a
for lib in "$bit7z_cov" "$bit7z_fuzz"; do
  llvm-nm --defined-only --demangle "$lib" > /work/bit7z-symbols.txt
  for sym in 'bit7z::Bit7zLibrary::Bit7zLibrary(' 'bit7z::BitInputArchive::~BitInputArchive()' \
             'bit7z::BitArchiveReader::BitArchiveReader(' 'bit7z::BitFormat::Zip'; do
    grep -qF "$sym" /work/bit7z-symbols.txt
  done
done
rm /work/bit7z-symbols.txt
llvm-readelf --section-headers "$bit7z_cov" | grep -qF __llvm_covfun
if ! llvm-readelf --section-headers "$bit7z_fuzz" | grep -qF __sancov_cntrs; then
  llvm-nm "$bit7z_fuzz" | grep -qF __afl_area_ptr
fi
if llvm-readelf --section-headers "$bit7z_cov" | grep -qF __sancov_cntrs ||
   llvm-readelf --section-headers "$bit7z_fuzz" | grep -qF __llvm_covfun; then
  echo 'bit7z coverage and sanitizer archives are mixed up' >&2
  exit 1
fi
defines='-D_FILE_OFFSET_BITS=64 -D_TIME_BITS=64'

$cxx -std=c++17 $base $coverage $defines -I/work/bit7z/include \
  '-DPARSARIUM_SEVENZIP_LIBRARY="/work/lib-cov/7z.so"' \
  /work/harness.cpp /work/replay.cpp "$bit7z_cov" \
  -Wl,--no-as-needed /work/lib-cov/7z.so -Wl,--as-needed -ldl -o /work/replay
$cxx -std=c++17 $base -fsanitize=fuzzer,address,undefined -fno-sanitize=alignment $defines -I/work/bit7z/include \
  '-DPARSARIUM_SEVENZIP_LIBRARY="/work/lib-fuzz/7z.so"' \
  /work/harness.cpp /work/fuzz.cpp "$bit7z_fuzz" \
  -Wl,--no-as-needed /work/lib-fuzz/7z.so -Wl,--as-needed -ldl -o /work/fuzzer

# The harness binaries must load the pinned 7z.so of their own build.
llvm-readelf --dynamic /work/replay | grep -F '[/work/lib-cov/7z.so]'
llvm-readelf --dynamic /work/fuzzer | grep -F '[/work/lib-fuzz/7z.so]'
