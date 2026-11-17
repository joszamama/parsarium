#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer'
poco() {
  cmake -S /work/source -B "/work/build-$1" \
    -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE=None -DCMAKE_C_FLAGS="$common $2" -DCMAKE_CXX_FLAGS="$common $2" \
    -DBUILD_SHARED_LIBS=OFF -DPOCO_UNBUNDLED=OFF \
    -DENABLE_JSON=ON -DENABLE_XML=OFF -DENABLE_NET=OFF -DENABLE_UTIL=OFF \
    -DENABLE_DATA=OFF -DENABLE_DATA_SQLITE=OFF -DENABLE_ZIP=OFF \
    -DENABLE_TESTS=OFF -DENABLE_SAMPLES=OFF -DENABLE_FUZZING=OFF > /dev/null
  cmake --build "/work/build-$1" --target JSON -j8 > /dev/null
}
case "${1:-}" in
  source)
    poco coverage '-fprofile-instr-generate -fcoverage-mapping'
    poco fuzzer '-fsanitize=fuzzer-no-link,address,undefined'
    ;;
  harness)
    coverage_libs='/work/build-coverage/lib/libPocoJSON.a /work/build-coverage/lib/libPocoFoundation.a'
    fuzzer_libs='/work/build-fuzzer/lib/libPocoJSON.a /work/build-fuzzer/lib/libPocoFoundation.a'
    includes='-I/work/source/JSON/include -I/work/source/Foundation/include -I/work/source/dependencies/tessil/include'
    clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping $includes \
      /work/harness.cpp $coverage_libs -pthread -ldl -o /work/replay
    clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined $includes \
      -DPARSARIUM_FUZZER /work/harness.cpp $fuzzer_libs -pthread -ldl -o /work/fuzzer
    clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping $includes \
      /work/parser-probe.cpp $coverage_libs -pthread -ldl -o /work/parser-probe
    clang++ -std=c++17 $common -fsanitize=address,undefined $includes \
      /work/parser-probe.cpp $fuzzer_libs -pthread -ldl -o /work/parser-probe-afl
    ;;
  *) echo 'usage: build.sh source|harness' >&2; exit 2 ;;
esac
