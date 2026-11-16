#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
harness_flags="$common -fsanitize=address,undefined"
cmake -S /work/source -B /work/build \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DCMAKE_INSTALL_PREFIX=/work -DBRLCAD_EXT_SOURCE_DIR=/work/bext \
  -DBRLCAD_EXT_PARALLEL=2 -DBRLCAD_ENABLE_MINIMAL=ON \
  -DBRLCAD_ENABLE_TCL=OFF -DBRLCAD_ENABLE_ASSETIMPORT=OFF \
  -DBRLCAD_ENABLE_STEP=OFF -DBRLCAD_ENABLE_GDAL=OFF \
  -DBRLCAD_ENABLE_OPENVDB=OFF -DBUILD_STATIC_LIBS=OFF \
  -DBRLCAD_VALIDATE_STATIC_LINKS=OFF \
  -DBRLCAD_ENABLE_ADDRESS_SANITIZER=ON
cmake --build /work/build --target gcv-ply -j 2

clang -std=c11 $harness_flags -I/work/source/include -I/work/build/include \
  -c /work/harness.c -o /work/harness.o
clang -std=c11 $harness_flags -c /work/replay.c -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o \
  -L/work/build/lib -Wl,-rpath,/work/lib -lgcv -lrt -lbu -o /work/replay

clang -std=c11 $harness_flags -c /work/fuzz.c -o /work/fuzz.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/fuzz.o \
  -L/work/build/lib -Wl,-rpath,/work/lib -lgcv -lrt -lbu -o /work/fuzzer
