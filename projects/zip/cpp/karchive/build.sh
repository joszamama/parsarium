#!/bin/sh
set -eu

# Build only the static KF6Archive library from the pinned KArchive source,
# twice: once with LLVM source coverage for the replay binary, and once with
# libFuzzer-compatible sanitizer instrumentation for the fuzzer. The optional
# bzip2, xz/7z, zstd and OpenSSL backends are disabled, so KZip's deflate path
# goes through KCompressionDevice and KGzipFilter to the distribution zlib.
# Qt6Core and zlib are the uninstrumented Ubuntu shared libraries.
cc=clang
cxx=clang++
jobs=${PARSARIUM_JOBS:-4}
base='-O1 -g -fno-omit-frame-pointer -DNDEBUG'
coverage='-fprofile-instr-generate -fcoverage-mapping'
fuzz='-fsanitize=fuzzer-no-link,address,undefined'

# Translations are not part of the parser; removing the catalogs avoids a
# configure-time dependency on Qt LinguistTools.
rm -rf /work/source/poqm

configure() {
  cmake -S /work/source -B "$1" -G 'Unix Makefiles' \
    -DCMAKE_BUILD_TYPE=None -DCMAKE_C_COMPILER=$cc -DCMAKE_CXX_COMPILER=$cxx \
    -DCMAKE_C_FLAGS="$base $2" -DCMAKE_CXX_FLAGS="$base $2" \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DBUILD_SHARED_LIBS=OFF -DBUILD_TESTING=OFF \
    -DECM_DIR=/work/ecm/share/ECM/cmake \
    -DWITH_BZIP2=OFF -DWITH_LIBLZMA=OFF -DWITH_OPENSSL=OFF -DWITH_LIBZSTD=OFF \
    -DCMAKE_DISABLE_FIND_PACKAGE_BZip2=ON -DCMAKE_DISABLE_FIND_PACKAGE_LibLZMA=ON \
    -DCMAKE_DISABLE_FIND_PACKAGE_OpenSSL=ON -DCMAKE_DISABLE_FIND_PACKAGE_PkgConfig=ON
  cmake --build "$1" --target KF6Archive -j "$jobs"
}
configure /work/build-cov "$coverage"
configure /work/build-fuzz "$fuzz"

# Every compiled KArchive translation unit must carry the requested flags, and
# no optional backend may have been picked up.
python3 - <<'PY'
import json

wanted = ("karchive.cpp", "kzip.cpp", "kcompressiondevice.cpp", "kfilterbase.cpp",
          "kgzipfilter.cpp", "klimitediodevice.cpp", "knonefilter.cpp",
          "kar.cpp", "ktar.cpp", "krcc.cpp")
for build, flag in (("/work/build-cov", "-fcoverage-mapping"),
                    ("/work/build-fuzz", "-fsanitize=fuzzer-no-link,address,undefined")):
    entries = json.load(open(f"{build}/compile_commands.json"))
    sources = {e["file"]: e.get("command") or " ".join(e["arguments"]) for e in entries}
    for name in wanted:
        path = f"/work/source/src/{name}"
        if path not in sources or flag not in sources[path]:
            raise SystemExit(f"uninstrumented or missing in {build}: {name}")
    extra = [p for p in sources if p.startswith("/work/source/src/")
             and p.rsplit("/", 1)[1] not in wanted]
    if extra:
        raise SystemExit(f"unexpected KArchive sources in {build}: {extra}")
PY

cov_lib=$(find /work/build-cov -name libKF6Archive.a)
fuzz_lib=$(find /work/build-fuzz -name libKF6Archive.a)
test -f "$cov_lib" && test -f "$fuzz_lib"
qt_cflags=$(pkg-config --cflags Qt6Core)
qt_libs=$(pkg-config --libs Qt6Core)

$cxx -std=c++20 -fPIC $base $coverage \
  -I/work/source/src -I/work/build-cov/src $qt_cflags \
  /work/harness.cpp /work/replay.cpp "$cov_lib" $qt_libs -lz -o /work/replay
$cxx -std=c++20 -fPIC $base -fsanitize=fuzzer,address,undefined \
  -I/work/source/src -I/work/build-fuzz/src $qt_cflags \
  /work/harness.cpp /work/fuzz.cpp "$fuzz_lib" $qt_libs -lz -o /work/fuzzer
