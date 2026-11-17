FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm make python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/jqlang/jq/releases/download/jq-1.8.2/jq-1.8.2.tar.gz --output /work/jq.tar.gz \
    && echo '71b8d6e8f5fe81f6c6d0d110e3892251f6ce76ed095abd315e26e6e1193af3af  /work/jq.tar.gz' | sha256sum --check \
    && tar -xf /work/jq.tar.gz -C /work && mv /work/jq-1.8.2 /work/jq-src
COPY harness.c parser-probe.c build.sh afl-allowlist.txt /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/parser-probe /work/afl-instrumented-objects.txt /work/
COPY --from=build /work/jq-src/src /work/jq-src/src
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh manifest.json /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
