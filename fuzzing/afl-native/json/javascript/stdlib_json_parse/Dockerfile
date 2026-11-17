# AFL++ target for the standard Node.js JSON.parse path: Node.js 26.10.0 built from the official source
# tarball with Clang 20.1 (same pin as projects/.../source-coverage). Only deps/v8/src/json/json-parser.cc
# carries SanitizerCoverage trace-pc-guard; the node executable links AFL++'s compiler runtime. The build
# fails unless json-parser.o is the single object with coverage guards and node links the AFL++ runtime.
# Build context: repository root (see build.py).
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    binutils=2.46-3ubuntu2 ca-certificates clang-20=1:20.1.8-2ubuntu8 libclang-rt-20-dev=1:20.1.8-2ubuntu8 \
    llvm-20=1:20.1.8-2ubuntu8 cargo=1.93.1ubuntu1 rustc=1.93.1ubuntu1 curl g++=4:15.2.0-5ubuntu1 make=4.4.1-3 \
    python3=3.14.3-0ubuntu2 xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://nodejs.org/dist/v26.10.0/node-v26.10.0.tar.xz --output node-v26.10.0.tar.xz \
    && echo '7b3a546d33cb7e15a43bdd7a57e0be5d5fd5ffc553e6e4c120033e66f0ba20c5  node-v26.10.0.tar.xz' | sha256sum --check \
    && tar -xJf node-v26.10.0.tar.xz && rm node-v26.10.0.tar.xz
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 \
    && rm -rf /var/lib/apt/lists/*
COPY fuzzing/afl-native/json/javascript/stdlib_json_parse/afl-cc.sh /opt/afl-cc/afl-cc.sh
RUN chmod 755 /opt/afl-cc/afl-cc.sh && ln -s afl-cc.sh /opt/afl-cc/cc && ln -s afl-cc.sh /opt/afl-cc/c++
WORKDIR /work/node-v26.10.0
RUN CC=/opt/afl-cc/cc CXX=/opt/afl-cc/c++ CC_host=/opt/afl-cc/cc CXX_host=/opt/afl-cc/c++ \
    ./configure --v8-enable-temporal-support --without-npm \
    && CC=/opt/afl-cc/cc CXX=/opt/afl-cc/c++ make -j"$(nproc)" -C out BUILDTYPE=Release node \
    && cp out/Release/node /work/node
# Gate: exactly one object (json-parser.o) carries __sancov_guards, no other object references the
# SanitizerCoverage callbacks, node links the AFL++ runtime, and node's one guard section is no larger
# than that object's (the linker may drop guards of unused functions).
RUN find out/Release -name '*.o' -print0 | xargs -0 -n 200 llvm-objdump-20 --section-headers \
       | awk '/file format/ {file = $1} /__sancov_guards/ {print file}' | sed 's/:$//' | sort -u > /work/instrumented-objects.txt \
    && cat /work/instrumented-objects.txt \
    && [ "$(wc -l < /work/instrumented-objects.txt)" = 1 ] \
    && grep -q '/json-parser\.o$' /work/instrumented-objects.txt \
    && find out/Release -name '*.o' ! -name json-parser.o -print0 | xargs -0 -n 200 llvm-nm-20 --undefined-only --no-sort 2>/dev/null \
       | { ! grep -q '__sanitizer_cov_'; } \
    && llvm-nm-20 --defined-only /work/node | grep -E ' (__afl_area_ptr|__sanitizer_cov_trace_pc_guard|__sanitizer_cov_trace_pc_guard_init)$' \
       | awk '{print $3}' | sort > /work/afl-runtime-symbols.txt \
    && [ "$(wc -l < /work/afl-runtime-symbols.txt)" = 3 ] \
    && object="$(cat /work/instrumented-objects.txt)" \
    && for size in $(llvm-objdump-20 --section-headers "$object" | awk '$2 == "__sancov_guards" {print $3}'); do \
         echo $((0x$size)); done > /work/object-guard-bytes.txt \
    && for size in $(llvm-objdump-20 --section-headers /work/node | awk '$2 == "__sancov_guards" {print $3}'); do \
         echo $((0x$size)); done > /work/node-guard-bytes.txt \
    && cat /work/object-guard-bytes.txt /work/node-guard-bytes.txt \
    && [ "$(wc -l < /work/node-guard-bytes.txt)" = 1 ] \
    && [ "$(cat /work/node-guard-bytes.txt)" -gt 0 ] \
    && [ "$(cat /work/node-guard-bytes.txt)" -le "$(awk '{s += $1} END {print s}' /work/object-guard-bytes.txt)" ]
RUN { /work/node --version; /work/node -p '"v8 " + process.versions.v8'; clang-20 --version | head -n 1; \
      rustc --version; cargo --version; \
      dpkg-query -W -f='${Package} ${Version}\n' clang-20 llvm-20 libclang-rt-20-dev rustc cargo afl++; } > /work/toolchain.txt \
    && sha256sum /work/node deps/v8/src/json/json-parser.cc deps/v8/src/json/json-parser.h /usr/lib/afl/afl-compiler-rt.o \
       > /work/source-hashes.txt \
    && cat /work/toolchain.txt /work/source-hashes.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends libatomic1=16-20260322-1ubuntu1 \
    afl++=4.33c-1.1ubuntu1 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /work/node /opt/node/bin/node
COPY --from=build /work/toolchain.txt /work/source-hashes.txt /work/instrumented-objects.txt \
     /work/afl-runtime-symbols.txt /work/object-guard-bytes.txt /work/node-guard-bytes.txt /work/
COPY projects/json/javascript/stdlib_json_parse/adapter.mjs /work/adapter.mjs
RUN echo 'e8e24e794840f27e21c13e9f7266c4803cf5976f9da2674fc6552d671d2c44e2  /work/adapter.mjs' | sha256sum --check \
    && grep ' /work/node$' /work/source-hashes.txt | sed 's| /work/node$| /opt/node/bin/node|' | sha256sum --check \
    && grep ' /usr/lib/afl/afl-compiler-rt.o$' /work/source-hashes.txt | sha256sum --check
WORKDIR /tmp
