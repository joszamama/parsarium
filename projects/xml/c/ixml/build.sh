#!/bin/sh
set -eu
# Configure pupnp with CMake for its generated headers, then build only the IXML static library.
cov='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
cmake -S /work/source -B /work/build -DCMAKE_C_COMPILER=clang -DCMAKE_BUILD_TYPE=None -DCMAKE_C_FLAGS="$cov" \
 -DUPNP_BUILD_SHARED=OFF -DUPNP_BUILD_STATIC=ON -DUPNP_BUILD_SAMPLES=OFF -DUPNP_ENABLE_TESTING=OFF -DUPNP_ENABLE_TESTING_INTEGRATION=OFF
cmake --build /work/build --target ixml_static -j 4
common='-O1 -g -fno-omit-frame-pointer'
inc='-I/work/source/ixml/inc -I/work/source/upnp/inc -I/work/build/upnp/inc -I/work/build'
clang $common -fprofile-instr-generate -fcoverage-mapping $inc /work/harness.c /work/replay.c /work/build/ixml/libixml.a -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -fprofile-instr-generate $inc /work/harness.c /work/build/ixml/libixml.a -o /work/fuzzer
