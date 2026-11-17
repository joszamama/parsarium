FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends bzip2 ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/pupnp/pupnp/releases/download/release-22.2.1/libupnp-22.2.1.tar.bz2 -o /work/source.tar.bz2 \
 && echo '11ac0f670aad96bd9c81cc84a6d4ae874a7b4b11073d5b88a03fd43efd097cc6  /work/source.tar.bz2' | sha256sum --check \
 && mkdir /work/source && tar -xjf /work/source.tar.bz2 -C /work/source --strip-components=1
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
