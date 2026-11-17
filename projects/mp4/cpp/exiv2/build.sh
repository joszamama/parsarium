#!/bin/sh
set -eu
src=/work/exiv2-0.28.9
common='-O1 -g -fno-omit-frame-pointer'
opts='-DBUILD_SHARED_LIBS=OFF -DEXIV2_ENABLE_VIDEO=ON -DEXIV2_ENABLE_FILESYSTEM_ACCESS=ON -DEXIV2_ENABLE_XMP=OFF -DEXIV2_ENABLE_EXTERNAL_XMP=OFF -DEXIV2_ENABLE_PNG=OFF -DEXIV2_ENABLE_BMFF=OFF -DEXIV2_ENABLE_BROTLI=OFF -DEXIV2_ENABLE_NLS=OFF -DEXIV2_ENABLE_INIH=OFF -DEXIV2_ENABLE_WEBREADY=OFF -DEXIV2_ENABLE_CURL=OFF -DEXIV2_ENABLE_LENSDATA=OFF -DEXIV2_BUILD_SAMPLES=OFF -DEXIV2_BUILD_EXIV2_COMMAND=OFF -DEXIV2_BUILD_UNIT_TESTS=OFF -DEXIV2_BUILD_FUZZ_TESTS=OFF -DEXIV2_BUILD_DOC=OFF -DBUILD_WITH_CCACHE=OFF'
cmake -S "$src" -B /work/coverage-build -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=None -DCMAKE_C_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" -DCMAKE_CXX_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" $opts
cmake --build /work/coverage-build --target exiv2lib -j 2
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping -I"$src/include" -I/work/coverage-build /work/harness.cpp /work/replay.cpp /work/coverage-build/lib/libexiv2.a -o /work/replay
cmake -S "$src" -B /work/fuzz-build -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=None -DCMAKE_C_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" -DCMAKE_CXX_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" $opts
cmake --build /work/fuzz-build --target exiv2lib -j 2
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -I"$src/include" -I/work/fuzz-build /work/harness.cpp /work/fuzz-build/lib/libexiv2.a -o /work/fuzzer
