#!/bin/sh
set -eu
CC=clang CXX=clang++ CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source/DevIL/src-IL -B /work/build -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_CXX_STANDARD=11 -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/work/install -DBUILD_SHARED_LIBS=OFF -DIL_NO_PNG=OFF -DIL_NO_TIF=ON -DIL_NO_JPG=ON -DIL_NO_EXR=ON -DIL_NO_JP2=ON -DIL_NO_MNG=ON -DIL_NO_LCMS=ON
cmake --build /work/build -j 4
cmake --install /work/build
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/install/include -c /work/harness.c -o /work/harness-cov.o
clang $common -fprofile-instr-generate -fcoverage-mapping -I/work/install/include -c /work/replay.c -o /work/replay-cov.o
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness-cov.o /work/replay-cov.o /work/install/lib/libIL.a -lpng -lz -lm -o /work/replay
clang $common -fsanitize=fuzzer-no-link,address,undefined -I/work/install/include -c /work/harness.c -o /work/harness-fuzz.o
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness-fuzz.o /work/install/lib/libIL.a -lpng -lz -lm -o /work/fuzzer
