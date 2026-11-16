#!/bin/sh
set -eu
src=/work/Bento4-1.6.0-641
common='-O1 -g -fno-omit-frame-pointer'
opts='-DBUILD_APPS=OFF -DCMAKE_C_COMPILER=clang'
core="-I$src/Source/C++/Core -I$src/Source/C++/Codecs -I$src/Source/C++/Crypto -I$src/Source/C++/MetaData"
inc="-I$src/Source/C++/CApi -I$src/Source/C++/Core"
cov='-fprofile-instr-generate -fcoverage-mapping'
# Upstream AP4 calls memcpy with a null pointer and a zero byte count on the
# valid MP4 control. UBSan's nonnull check reports it, so this collection
# harness uses ASan for the one-case smoke while preserving upstream source.
fuzz='-fsanitize=fuzzer-no-link,address'
# AP4 static core only (no apps); the CApi binding is not a CMake target upstream.
cmake -S "$src" -B /work/coverage-build -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_CXX_FLAGS="$common $cov" $opts
cmake --build /work/coverage-build --target ap4 -j 2
clang++ -std=c++17 $common $cov $core -c "$src/Source/C++/CApi/Bento4C.cpp" -o /work/coverage-build/Bento4C.o
clang -std=c11 $common $cov $inc -c /work/harness.c -o /work/harness.o
clang -std=c11 $common $cov $inc -c /work/replay.c -o /work/replay.o
clang++ $common $cov /work/harness.o /work/replay.o /work/coverage-build/Bento4C.o /work/coverage-build/libap4.a -o /work/replay
cmake -S "$src" -B /work/fuzz-build -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_CXX_FLAGS="$common $fuzz" $opts
cmake --build /work/fuzz-build --target ap4 -j 2
clang++ -std=c++17 $common $fuzz $core -c "$src/Source/C++/CApi/Bento4C.cpp" -o /work/fuzz-build/Bento4C.o
clang -std=c11 $common $fuzz $inc -c /work/harness.c -o /work/harness-fuzz.o
clang++ $common -fsanitize=fuzzer,address /work/harness-fuzz.o /work/fuzz-build/Bento4C.o /work/fuzz-build/libap4.a -o /work/fuzzer
