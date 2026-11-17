#!/bin/sh
set -eu

# One libwebsockets build carries LLVM source coverage for replay and sanitizer
# coverage for the fuzzer, so both binaries exercise instrumented lws code.
# The out-of-tree build keeps absolute /work/source paths in coverage data.
# Only the plain-TCP HTTP/1 server role is built: no TLS, client, HTTP/2,
# HTTP/3, Secure Streams, image decoders or netlink monitor.
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
cmake -S /work/source -B /work/lws-build \
  -DCMAKE_BUILD_TYPE=None \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS="$common" \
  -DCMAKE_EXE_LINKER_FLAGS="$common" \
  -DDISABLE_WERROR=ON \
  -DLWS_WITH_STATIC=ON -DLWS_WITH_SHARED=OFF \
  -DLWS_WITH_SSL=OFF -DLWS_WITHOUT_CLIENT=ON \
  -DLWS_ROLE_H1=ON -DLWS_ROLE_WS=ON -DLWS_WITH_HTTP2=OFF \
  -DLWS_WITH_HTTP3=OFF -DLWS_ROLE_QUIC=OFF \
  -DLWS_WITH_HTTP_UNCOMMON_HEADERS=ON \
  -DLWS_WITH_SECURE_STREAMS=OFF -DLWS_WITH_NETLINK=OFF \
  -DLWS_WITH_UPNG=OFF -DLWS_WITH_JPEG=OFF -DLWS_WITH_DLO=OFF \
  -DLWS_WITH_SYS_SMD=OFF -DLWS_WITH_CONMON=OFF -DLWS_WITH_CACHE_NSCOOKIEJAR=OFF \
  -DLWS_WITHOUT_TESTAPPS=ON -DLWS_WITH_MINIMAL_EXAMPLES=OFF \
  -DLWS_WITH_LWSWS=OFF -DLWS_WITH_PLUGINS=OFF -DLWS_WITH_EVLIB_PLUGINS=OFF
cmake --build /work/lws-build --target websockets -j 4

lws='/work/lws-build/lib/libwebsockets.a'
lws_includes='-I/work/lws-build/include'

clang++ -std=c++17 $common $lws_includes -c /work/harness.cpp -o /work/harness.o
clang++ -std=c++17 $common -c /work/replay.cpp -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o "$lws" -pthread -o /work/replay

clang++ -std=c++17 $common -c /work/fuzz.cpp -o /work/fuzz.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o "$lws" -pthread -o /work/fuzzer
