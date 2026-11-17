#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
cmake -S /work/source -B /work/build \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DDEFAULT=OFF -DENABLE_BUILD_SHARED=ON -DENABLE_MESH=ON \
  -DENABLE_PARSER=OFF -DENABLE_POST=OFF -DENABLE_EIGEN=OFF \
  -DENABLE_GMP=OFF -DGMSH_RELEASE=ON
cmake --build /work/build --target shared -j 2
mkdir -p /work/lib
cp -a /work/build/libgmsh.so* /work/lib/

clang -std=c11 $common -I/work/source/api -c /work/harness.c -o /work/harness.o
clang -std=c11 $common -c /work/replay.c -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o \
  -L/work/lib -Wl,-rpath,/work/lib -lgmsh -o /work/replay

clang -std=c11 $common -c /work/fuzz.c -o /work/fuzz.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o \
  -L/work/lib -Wl,-rpath,/work/lib -lgmsh -o /work/fuzzer
