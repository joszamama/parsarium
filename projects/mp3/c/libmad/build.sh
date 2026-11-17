#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
cmake -S /work/source -B /work/build -DCMAKE_C_COMPILER=clang -DCMAKE_BUILD_TYPE=None \
 -DCMAKE_C_FLAGS="$common -fprofile-instr-generate -fcoverage-mapping" \
 -DBUILD_SHARED_LIBS=OFF -DEXAMPLE=OFF -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib
cmake --build /work/build -j 4
cmake --install /work/build
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/install/include /work/harness.c /work/replay.c /work/install/lib/libmad.a -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -I/work/install/include /work/harness.c /work/install/lib/libmad.a -o /work/fuzzer
