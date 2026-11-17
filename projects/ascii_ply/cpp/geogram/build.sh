#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
fuzz_flags="$common -fsanitize=fuzzer-no-link,address,undefined"
cmake -S /work/source -B /work/build \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DVORPALINE_PLATFORM=Linux64-nonx86-clang-dynamic \
  -DGEOGRAM_WITH_GRAPHICS=OFF -DGEOGRAM_WITH_LEGACY_NUMERICS=OFF \
  -DGEOGRAM_WITH_HLBFGS=OFF -DGEOGRAM_WITH_TETGEN=OFF \
  -DGEOGRAM_WITH_TRIANGLE=OFF -DGEOGRAM_WITH_LUA=OFF \
  -DGEOGRAM_WITH_EXPLORAGRAM=OFF -DGEOGRAM_LIB_ONLY=ON
cmake --build /work/build --target geogram -j 2

clang++ -std=c++17 $common -I/work/source/src/lib \
  -c /work/harness.cpp -o /work/harness-coverage.o
clang++ -std=c++17 $common -c /work/replay.cpp -o /work/replay.o
clang++ $common /work/harness-coverage.o /work/replay.o \
  -L/work/build/lib -Wl,-rpath,/work/lib -lgeogram -ldl -lpthread \
  -o /work/replay

clang++ -std=c++17 $fuzz_flags -I/work/source/src/lib \
  -c /work/harness.cpp -o /work/harness-fuzz.o
clang++ -std=c++17 $fuzz_flags -c /work/fuzz.cpp -o /work/fuzz.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness-fuzz.o /work/fuzz.o \
  -L/work/build/lib -Wl,-rpath,/work/lib -lgeogram -ldl -lpthread \
  -o /work/fuzzer
