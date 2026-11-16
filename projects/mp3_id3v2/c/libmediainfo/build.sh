#!/bin/sh
set -eu
cmake -S /work/source/Project/CMake -B /work/build -G Ninja \
 -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=/work/install \
 -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
 -DCMAKE_C_FLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 -DCMAKE_CXX_FLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
cmake --build /work/build -j 4
cmake --install /work/build
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig:/work/install/lib/aarch64-linux-gnu/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/install/include -c /work/harness.c -o /work/harness-cov.o
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/install/include -c /work/replay.c -o /work/replay-cov.o
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness-cov.o /work/replay-cov.o /work/install/lib/libmediainfo.a -lzen -lz -lpthread -ldl -o /work/replay
clang $common -fsanitize=fuzzer-no-link,address,undefined -I/work/install/include -c /work/harness.c -o /work/harness-fuzz.o
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness-fuzz.o /work/install/lib/libmediainfo.a -lzen -lz -lpthread -ldl -o /work/fuzzer
