#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
cmake -S /work/source -B /work/cov-build -DCMAKE_C_COMPILER=clang -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DCMAKE_C_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" \
  -DENABLE_EXTERNAL_LIBS=OFF -DENABLE_MPEG=ON -DBUILD_TESTING=OFF \
  -DBUILD_PROGRAMS=OFF -DBUILD_EXAMPLES=OFF -DBUILD_SHARED_LIBS=OFF
cmake --build /work/cov-build --target sndfile -j 2
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/source/include \
  /work/harness.c /work/replay.c /work/cov-build/libsndfile.a -lmpg123 -lmp3lame -lm -o /work/replay
cmake -S /work/source -B /work/fuzz-build -DCMAKE_C_COMPILER=clang -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DCMAKE_C_FLAGS="$common -fsanitize=fuzzer-no-link,address,undefined" \
  -DENABLE_EXTERNAL_LIBS=OFF -DENABLE_MPEG=ON -DBUILD_TESTING=OFF \
  -DBUILD_PROGRAMS=OFF -DBUILD_EXAMPLES=OFF -DBUILD_SHARED_LIBS=OFF
cmake --build /work/fuzz-build --target sndfile -j 2
clang $common -fsanitize=fuzzer,address,undefined -I/work/source/include \
  /work/harness.c /work/fuzz-build/libsndfile.a -lmpg123 -lmp3lame -lm -o /work/fuzzer
