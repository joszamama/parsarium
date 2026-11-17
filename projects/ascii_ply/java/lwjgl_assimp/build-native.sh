#!/bin/sh
set -eu

# Rebuild the libassimp.so/libdraco.so pair that natives-linux-arm64 bundles, from the
# LWJGL-CI/assimp commit the jar names, with the LWJGL CI CMake options. Only the compiler
# (clang instead of GCC 12) and the LLVM coverage flags differ; the C API, the headers and
# the importer set stay the same, so LWJGL binds to the rebuilt library unchanged.
coverage='-g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
cmake -S /work/source -B /work/assimp-build \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="-U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0 $coverage" \
  -DCMAKE_CXX_FLAGS="$coverage" \
  -DCMAKE_C_FLAGS_RELEASE='-O1 -DNDEBUG' -DCMAKE_CXX_FLAGS_RELEASE='-O1 -DNDEBUG' \
  -DCMAKE_SHARED_LINKER_FLAGS='-fprofile-instr-generate' \
  -DASSIMP_BUILD_ASSIMP_TOOLS=OFF -DASSIMP_BUILD_TESTS=OFF \
  -DASSIMP_BUILD_DRACO=ON -DASSIMP_BUILD_ZLIB=ON \
  -DASSIMP_IGNORE_GIT_HASH=ON -DASSIMP_WARNINGS_AS_ERRORS=OFF
cmake --build /work/assimp-build -j 4

mkdir /work/native
cp -L /work/assimp-build/bin/libassimp.so /work/native/libassimp.so
cp -L /work/assimp-build/bin/libdraco.so /work/native/libdraco.so
cp /work/native-stock/liblwjgl.so /work/native/liblwjgl.so

# The rebuilt pair must keep the stock dependency shape and export every ai* entry point
# of the stock library, because LWJGL resolves all of them when org.lwjgl.assimp.Assimp loads.
soname() { readelf -d "$1" | sed -n 's/.*(SONAME).*\[\(.*\)\]/\1/p'; }
needed() { readelf -d "$1" | sed -n 's/.*(NEEDED).*\[\(libdraco[^]]*\)\]/\1/p'; }
test "$(soname /work/native/libassimp.so)" = "$(soname /work/native-stock/libassimp.so)"
test "$(needed /work/native/libassimp.so)" = "$(soname /work/native/libdraco.so)"
test "$(needed /work/native-stock/libassimp.so)" = "$(soname /work/native-stock/libdraco.so)"
exports() { nm -D --defined-only "$1" | awk '$3 ~ /^ai/ {print $3}' | sort -u; }
exports /work/native-stock/libassimp.so > /work/abi-stock-exports.txt
exports /work/native/libassimp.so > /work/abi-built-exports.txt
missing=$(comm -23 /work/abi-stock-exports.txt /work/abi-built-exports.txt)
if [ -n "$missing" ]; then
  echo "instrumented libassimp.so lacks stock exports: $missing" >&2
  exit 1
fi
nm /work/native/libassimp.so | grep -q __llvm_profile_runtime

# Header struct layout versus the layout LWJGL computes in Java.
clang -std=c11 -I/work/source/include -I/work/assimp-build/include \
  /work/abi_layout.c -o /work/abi_layout
/work/abi_layout > /work/abi-native-layout.json
java -Dorg.lwjgl.librarypath=/work/native-stock -cp '/work/classes:/work/lib/*' \
  AbiLayout > /work/abi-lwjgl-layout.json
python3 - <<'PY'
import json
native = json.load(open('/work/abi-native-layout.json'))
lwjgl = json.load(open('/work/abi-lwjgl-layout.json'))
if native != lwjgl:
    raise SystemExit(f'struct layout mismatch: native={native} lwjgl={lwjgl}')
json.dump({'struct_layout': native, 'stock_ai_exports': len(open('/work/abi-stock-exports.txt').read().split()),
           'built_ai_exports': len(open('/work/abi-built-exports.txt').read().split())},
          open('/work/abi-check.json', 'w'), indent=2)
PY
