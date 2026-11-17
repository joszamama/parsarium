#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
cmake -S /work/source -B /work/build -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DwxBUILD_TOOLKIT=gtk3 -DwxBUILD_SHARED=OFF -DwxBUILD_PRECOMP=OFF \
  -DwxBUILD_SAMPLES=OFF -DwxBUILD_TESTS=OFF -DwxBUILD_DEMOS=OFF \
  -DwxUSE_IMAGE=ON -DwxUSE_NANOSVG=builtin -DwxUSE_LUNASVG=OFF \
  -DwxUSE_PNG=OFF -DwxUSE_JPEG=OFF -DwxUSE_TIFF=OFF -DwxUSE_WEBP=OFF

# Fail early unless the generated setup.h selects the bundled NanoSVG backend.
setup=$(find /work/build/lib/wx/include -path '*/wx/setup.h' | head -n 1)
grep -Eq '^#define wxUSE_NANOSVG 1$' "$setup"
grep -Eq '^#define wxUSE_NANOSVG_EXTERNAL 0$' "$setup"
grep -Eq '^#define wxUSE_LUNASVG 0$' "$setup"

cmake --build /work/build --target wxcore -j 3

wx_flags=$(/work/build/wx-config --cxxflags)
wx_libs=$(/work/build/wx-config --libs core,base)
clang++ -std=c++17 $common $wx_flags -c /work/harness.cpp -o /work/harness.o
clang++ -std=c++17 $common $wx_flags -c /work/replay.cpp -o /work/replay.o
clang++ $common -Wl,--export-dynamic /work/harness.o /work/replay.o \
  $wx_libs -o /work/replay-bin

clang++ -std=c++17 $common -fsanitize=fuzzer-no-link,address,undefined \
  $wx_flags -c /work/harness.cpp -o /work/harness-fuzz.o
clang++ -std=c++17 $common -fsanitize=fuzzer-no-link,address,undefined \
  $wx_flags -c /work/fuzz.cpp -o /work/fuzz.o
clang++ $common -fsanitize=fuzzer,address,undefined -Wl,--export-dynamic \
  /work/harness-fuzz.o /work/fuzz.o $wx_libs -o /work/fuzzer-bin
