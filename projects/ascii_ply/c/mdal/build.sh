#!/bin/sh
set -eu

src=/work/MDAL-release-1.3.3
common='-O1 -g -fno-omit-frame-pointer'
options='-DENABLE_TESTS=OFF -DWITH_HDF5=OFF -DWITH_GDAL=OFF -DWITH_NETCDF=OFF -DWITH_XML=OFF -DWITH_SQLITE3=OFF -DBUILD_STATIC=ON -DBUILD_SHARED=OFF -DBUILD_TOOLS=OFF -DBUILD_EXTERNAL_DRIVERS=OFF -DBUILD_PLY=ON'

cmake -S "$src" -B /work/coverage-build $options \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_CXX_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping"
cmake --build /work/coverage-build --target mdal_a -j 2
clang -std=c11 $common -fprofile-instr-generate -fcoverage-mapping \
  -c /work/harness.c -o /work/harness-coverage.o
clang -std=c11 $common -fprofile-instr-generate -fcoverage-mapping \
  -c /work/replay.c -o /work/replay-coverage.o
clang++ $common -fprofile-instr-generate -fcoverage-mapping \
  /work/harness-coverage.o /work/replay-coverage.o \
  /work/coverage-build/mdal/libmdal_a.a -ldl -o /work/replay

cmake -S "$src" -B /work/fuzz-build $options \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_CXX_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined -fno-sanitize=alignment"
cmake --build /work/fuzz-build --target mdal_a -j 2
clang -std=c11 $common -fsanitize=fuzzer-no-link,address,undefined -fno-sanitize=alignment \
  -c /work/harness.c -o /work/harness-fuzz.o
clang -std=c11 $common -fsanitize=fuzzer-no-link,address,undefined -fno-sanitize=alignment \
  -c /work/fuzz.c -o /work/fuzz.o
clang++ $common -fsanitize=fuzzer,address,undefined -fno-sanitize=alignment \
  /work/harness-fuzz.o /work/fuzz.o /work/fuzz-build/mdal/libmdal_a.a \
  -ldl -o /work/fuzzer
