#!/bin/sh
set -eu
options='-DJAS_ENABLE_SHARED=OFF -DJAS_ENABLE_DOC=OFF -DJAS_ENABLE_PROGRAMS=OFF -DJAS_ENABLE_LIBJPEG=OFF -DJAS_ENABLE_LIBHEIF=OFF -DJAS_ENABLE_OPENGL=OFF -DJAS_ENABLE_MULTITHREADING_SUPPORT=OFF -DJAS_INCLUDE_BMP_CODEC=OFF -DJAS_INCLUDE_JP2_CODEC=OFF -DJAS_INCLUDE_JPC_CODEC=OFF -DJAS_INCLUDE_JPG_CODEC=OFF -DJAS_INCLUDE_HEIC_CODEC=OFF -DJAS_INCLUDE_MIF_CODEC=OFF -DJAS_INCLUDE_PGX_CODEC=OFF -DJAS_INCLUDE_RAS_CODEC=OFF -DJAS_INCLUDE_PNM_CODEC=ON -DJAS_ENABLE_PNM_CODEC=ON'
cmake -S /work/source -B /work/build-cov -DCMAKE_C_COMPILER=clang -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' $options
cmake --build /work/build-cov --target libjasper -j4
cmake -S /work/source -B /work/build-fuzz -DCMAKE_C_COMPILER=clang -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_FLAGS='-O1 -g -fsanitize=fuzzer-no-link,address,undefined' $options
cmake --build /work/build-fuzz --target libjasper -j4
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping -I/work/source/src/libjasper/include -I/work/build-cov/src/libjasper/include \
  /work/harness.c /work/replay.c /work/build-cov/src/libjasper/libjasper.a -lm -o /work/replay
clang -O1 -g -fsanitize=fuzzer,address,undefined -I/work/source/src/libjasper/include -I/work/build-fuzz/src/libjasper/include \
  /work/harness.c /work/build-fuzz/src/libjasper/libjasper.a -lm -o /work/fuzzer
