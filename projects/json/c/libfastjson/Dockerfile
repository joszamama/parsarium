FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm make python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://download.rsyslog.com/libfastjson/libfastjson-1.2609.0.tar.gz --output /work/libfastjson.tar.gz \
    && echo '7cd6f78c1c07f4140f6976a9a0e0048bcaa7292329c6ac2c0e070383d83d8edd  /work/libfastjson.tar.gz' | sha256sum --check \
    && tar -xf /work/libfastjson.tar.gz -C /work && mv /work/libfastjson-1.2609.0 /work/libfastjson-src
COPY harness.c parser-probe.c emit.h build.sh afl-allowlist.txt /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/parser-probe /work/afl-instrumented-objects.txt /work/
COPY --from=build /work/libfastjson-src /work/libfastjson-src
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh manifest.json /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
