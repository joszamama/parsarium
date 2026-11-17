#!/bin/sh
set -eu

# Serf ships an SCons build that also links OpenSSL for its TLS buckets. The
# response parser needs only the bucket sources below, so they are compiled
# directly with the same instrumentation as the harness: LLVM source coverage
# for replay and sanitizer coverage for the fuzzer.
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
apr_cflags=$(pkg-config --cflags apr-1 apr-util-1)
deps="$(pkg-config --libs apr-1 apr-util-1) -lz"
serf_sources='allocator buckets simple_buckets response_buckets headers_buckets
  barrier_buckets response_body_buckets limit_buckets dechunk_buckets deflate_buckets
  aggregate_buckets iovec_buckets'

mkdir -p /work/serf-build
serf_objects=''
for name in $serf_sources; do
  clang -std=gnu89 $common $apr_cflags -I/work/source \
    -c "/work/source/buckets/$name.c" -o "/work/serf-build/$name.o"
  serf_objects="$serf_objects /work/serf-build/$name.o"
done

clang++ -std=c++17 $common $apr_cflags -I/work/source \
  -c /work/harness.cpp -o /work/harness.o
clang++ -std=c++17 $common -c /work/replay.cpp -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o $serf_objects $deps -o /work/replay

clang++ -std=c++17 $common -c /work/fuzz.cpp -o /work/fuzz.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o $serf_objects $deps -o /work/fuzzer
