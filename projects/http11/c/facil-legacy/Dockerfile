FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/boazsegev/facil.io/archive/refs/tags/0.7.6.tar.gz \
    --output /work/facil.io-0.7.6.tar.gz \
    && echo 'dc004017093e1ae3838b8c2a281d77d7cc94a84e0f157d93740838fb61e26d47  /work/facil.io-0.7.6.tar.gz' | sha256sum --check \
    && mkdir /work/source \
    && tar -xzf /work/facil.io-0.7.6.tar.gz -C /work/source --strip-components=1 \
    && echo '04844b41f18de82ca592fcba0cb5fbe4fd0c9447e7bd3bd8ac706bcbb1474339  /work/source/lib/facil/http/parsers/http1_parser.h' | sha256sum --check \
    && echo '49e79d570836baba8a321c4e5ecc662970964170152c6e7ac6eaa664d98c6eed  /work/source/LICENSE' | sha256sum --check
COPY harness.h harness.c replay.c fuzz.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source/LICENSE /work/source/LICENSE
COPY --from=build /work/source/lib/facil/http/parsers /work/source/lib/facil/http/parsers
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
