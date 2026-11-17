FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/h2o/h2o/archive/refs/tags/v2.2.6.tar.gz \
    -o /work/source.tar.gz \
    && echo 'f8cbc1b530d85ff098f6efc2c3fdbc5e29baffb30614caac59d5c710f7bda201  /work/source.tar.gz' | sha256sum --check \
    && tar -xzf /work/source.tar.gz -C /work h2o-2.2.6/LICENSE h2o-2.2.6/deps/picohttpparser \
    && echo 'e17097b2385400d68969f125a04689e7f01bd562f1830c6fab4f3abe60ea5500  /work/h2o-2.2.6/deps/picohttpparser/picohttpparser.c' | sha256sum --check \
    && echo '288fc72b2a4850b0a65e32ee6b01970af55947186b8c8e17e585024074cb4aef  /work/h2o-2.2.6/deps/picohttpparser/picohttpparser.h' | sha256sum --check
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/h2o-2.2.6 /work/h2o-2.2.6
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
