# Node.js 26.10.0 built from the official source tarball with Clang 20.1 (the compiler family of the
# official linux-arm64 release). Only deps/v8/src/json/json-parser.cc carries Clang source-based
# coverage; the build fails unless that is the single instrumented object.
# Build context: projects/json/javascript/stdlib_json_parse (see run-smoke.sh).
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
COPY source-coverage/instrument-cc.sh /opt/cov/instrument-cc.sh
RUN chmod 755 /opt/cov/instrument-cc.sh && ln -s instrument-cc.sh /opt/cov/cc && ln -s instrument-cc.sh /opt/cov/c++
WORKDIR /work/node-v26.10.0
RUN CC=/opt/cov/cc CXX=/opt/cov/c++ CC_host=/opt/cov/cc CXX_host=/opt/cov/c++ \
    ./configure --v8-enable-temporal-support --without-npm \
    && CC=/opt/cov/cc CXX=/opt/cov/c++ make -j"$(nproc)" -C out BUILDTYPE=Release node \
    && cp out/Release/node /work/node
RUN find out/Release -name '*.o' -print0 | xargs -0 -n 200 llvm-objdump-20 --section-headers \
       | awk '/file format/ {file = $1} /__llvm_covfun/ {print file}' | sed 's/:$//' | sort -u > /work/instrumented-objects.txt \
    && cat /work/instrumented-objects.txt \
    && [ "$(wc -l < /work/instrumented-objects.txt)" = 1 ] \
    && grep -q '/json-parser\.o$' /work/instrumented-objects.txt
RUN { /work/node --version; /work/node -p '"v8 " + process.versions.v8'; clang-20 --version | head -n 1; \
      rustc --version; cargo --version; dpkg-query -W -f='${Package} ${Version}\n' clang-20 llvm-20 libclang-rt-20-dev rustc cargo; } > /work/toolchain.txt \
    && sha256sum /work/node deps/v8/src/json/json-parser.cc deps/v8/src/json/json-parser.h > /work/source-hashes.txt \
    && cat /work/toolchain.txt /work/source-hashes.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends libatomic1=16-20260322-1ubuntu1 llvm-20=1:20.1.8-2ubuntu8 \
    python3=3.14.3-0ubuntu2 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /work/node /opt/node/bin/node
COPY --from=build /work/toolchain.txt /work/source-hashes.txt /work/instrumented-objects.txt /work/
COPY --from=build /work/node-v26.10.0/deps/v8/src/json/json-parser.cc /work/node-v26.10.0/deps/v8/src/json/json-parser.h /work/node-v26.10.0/deps/v8/src/json/
COPY adapter.mjs second-control.json /work/
COPY source-coverage/measure.py /work/
RUN echo 'e8e24e794840f27e21c13e9f7266c4803cf5976f9da2674fc6552d671d2c44e2  /work/adapter.mjs' | sha256sum --check \
    && echo 'a54ab095e6fd9281696c461d7385b759b99129ccd14d5242de084e5868dc7762  /work/second-control.json' | sha256sum --check \
    && sed 's| /work/node$| /opt/node/bin/node|; s| deps/| /work/node-v26.10.0/deps/|' /work/source-hashes.txt | sha256sum --check
ENTRYPOINT ["python3", "-I", "/work/measure.py"]
