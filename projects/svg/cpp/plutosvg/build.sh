#!/bin/sh
set -eu
src=/work/plutosvg-0.0.8
common='-O1 -g -fno-omit-frame-pointer'
opts='-DBUILD_SHARED_LIBS=OFF -DPLUTOSVG_BUILD_EXAMPLES=OFF'
cmake -S "$src" -B /work/coverage-build -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" $opts
cmake --build /work/coverage-build --target plutosvg -j 2
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping \
  -I"$src/source" -I"$src/plutovg/include" /work/harness.cpp /work/replay.cpp \
  /work/coverage-build/libplutosvg.a /work/coverage-build/plutovg/libplutovg.a \
  -lm -o /work/replay
cmake -S "$src" -B /work/fuzz-build -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" $opts
cmake --build /work/fuzz-build --target plutosvg -j 2
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined \
  -I"$src/source" -I"$src/plutovg/include" /work/harness.cpp \
  /work/fuzz-build/libplutosvg.a /work/fuzz-build/plutovg/libplutovg.a \
  -lm -o /work/fuzzer
