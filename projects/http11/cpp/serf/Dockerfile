FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    bzip2 ca-certificates clang curl libapr1-dev libaprutil1-dev libclang-rt-21-dev llvm \
    pkg-config python3 zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://archive.apache.org/dist/serf/serf-1.3.10.tar.bz2 \
    --output /work/serf-1.3.10.tar.bz2 \
    && echo 'be81ef08baa2516ecda76a77adf7def7bc3227eeb578b9a33b45f7b41dc064e6  /work/serf-1.3.10.tar.bz2' | sha256sum --check \
    && mkdir /work/source \
    && tar -xjf /work/serf-1.3.10.tar.bz2 -C /work/source --strip-components=1 \
    && echo 'a6ec8199693a650c53e9703ff571f93218eb07340aa474ab24aa1fd2831139fb  /work/source/buckets/response_buckets.c' | sha256sum --check \
    && echo '29623e438a4dc8a8c90dc380536d1e3a4dcd74cda1832c682cc46e5ca2c844f7  /work/source/buckets/headers_buckets.c' | sha256sum --check \
    && echo '5cf5c16e264713de089546b87c6be49eabca25841de0fddc2caedf03f002f2b7  /work/source/buckets/buckets.c' | sha256sum --check
COPY harness.h harness.cpp replay.cpp fuzz.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libapr1t64 libaprutil1t64 libstdc++6 llvm python3 zlib1g \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
