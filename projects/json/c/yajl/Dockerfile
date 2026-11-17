FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/lloyd/yajl/archive/refs/tags/2.1.0.tar.gz --output /work/yajl.tar.gz \
    && echo '3fb73364a5a30efe615046d07e6db9d09fd2b41c763c5f7d3bfb121cd5c5ac5a  /work/yajl.tar.gz' | sha256sum --check \
    && tar -xf /work/yajl.tar.gz -C /work && mv /work/yajl-2.1.0 /work/yajl-src
COPY harness.c parser-probe.c emit.h build.sh afl-allowlist.txt /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/parser-probe /work/afl-instrumented-objects.txt /work/
COPY --from=build /work/yajl-src /work/yajl-src
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh manifest.json /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
