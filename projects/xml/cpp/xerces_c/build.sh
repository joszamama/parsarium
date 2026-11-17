#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
# Static library, no network accessor, GNU iconv transcoder; built once per instrumentation.
xerces() {
  cmake -S /work/source -B "/work/build-$1" -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE=None -DCMAKE_C_FLAGS="$common $2" -DCMAKE_CXX_FLAGS="$common $2" \
    -DBUILD_SHARED_LIBS=OFF -Dnetwork=OFF -Dtranscoder=gnuiconv -Dmessage-loader=inmemory > /dev/null
  cmake --build "/work/build-$1" --target xerces-c -j "$(nproc)" > /dev/null
}
xerces coverage '-fprofile-instr-generate -fcoverage-mapping'
xerces fuzzer '-fsanitize=fuzzer-no-link,address,undefined'
includes='-I/work/source/src -I/work/build-coverage/src'
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping $includes \
  /work/harness.cpp /work/replay.cpp /work/build-coverage/src/libxerces-c.a -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -I/work/source/src -I/work/build-fuzzer/src \
  /work/harness.cpp /work/build-fuzzer/src/libxerces-c.a -o /work/fuzzer
