#!/bin/sh
set -eu

# Build libpdalcpp.so.20 from the pinned PDAL 2.10.2 release with LLVM source coverage.
# pdal-native 2.10.0 ships only the JNI glue (libpdaljni.2.10.so, NEEDED libpdalcpp.so.20);
# PDAL itself is a separate native prerequisite, so the coverage build is the PDAL that the
# unmodified JNI library loads. Only the core library target is built (readers.ply is a
# built-in stage of libpdalcpp); plugins, tools and tests are off.
coverage='-g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
cmake -S /work/source -B /work/pdal-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$coverage" -DCMAKE_CXX_FLAGS="$coverage" \
  -DCMAKE_C_FLAGS_RELEASE='-O1 -DNDEBUG' -DCMAKE_CXX_FLAGS_RELEASE='-O1 -DNDEBUG' \
  -DCMAKE_SHARED_LINKER_FLAGS='-fprofile-instr-generate' \
  -DCMAKE_INSTALL_PREFIX=/work/pdal \
  -DWITH_TESTS=OFF -DWITH_COMPLETION=OFF -DBUILD_DOCS=OFF -DENABLE_CTEST=OFF \
  -DBUILD_TOOLS_LASDUMP=OFF -DBUILD_TOOLS_NITFWRAP=OFF -DWITH_GCS=OFF -DWITH_BACKTRACE=OFF
cmake --build /work/pdal-build --target pdalcpp -j "$(nproc)"

mkdir -p /work/native
cp -L "$(find /work/pdal-build -name 'libpdalcpp.so.20' | head -1)" /work/native/libpdalcpp.so.20
soname() { readelf -d "$1" | sed -n 's/.*(SONAME).*\[\(.*\)\]/\1/p'; }
test "$(soname /work/native/libpdalcpp.so.20)" = libpdalcpp.so.20
nm /work/native/libpdalcpp.so.20 | grep -q __llvm_profile_runtime

# The unmodified JNI library from pdal-native-2.10.0.jar must resolve every PDAL symbol it
# imports from the source-built library.
readelf -d /work/jni/libpdaljni.2.10.so | grep -q 'NEEDED.*\[libpdalcpp.so.20\]'
nm -D --undefined-only /work/jni/libpdaljni.2.10.so | awk '{print $2}' | grep '^_ZN4pdal\|^_ZNK4pdal' \
  | sed 's/@.*//' | sort -u > /work/jni-pdal-imports.txt
nm -D --defined-only /work/native/libpdalcpp.so.20 | awk '{print $3}' | sed 's/@.*//' | sort -u \
  > /work/pdal-exports.txt
missing=$(comm -23 /work/jni-pdal-imports.txt /work/pdal-exports.txt)
if [ -n "$missing" ]; then
  echo "source-built libpdalcpp lacks JNI imports: $missing" >&2
  exit 1
fi
printf '{"jni_pdal_imports": %s, "missing": 0}\n' "$(wc -l < /work/jni-pdal-imports.txt)" \
  > /work/abi-check.json
