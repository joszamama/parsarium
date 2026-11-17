FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl git libclang-rt-21-dev llvm make python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/recp/AssetKit/archive/refs/tags/v0.7.4.tar.gz \
    --output /work/AssetKit-0.7.4.tar.gz \
    && echo '6a0325976d46a30e6369c9718e31122e87f071ee3af114675ac43fb8b9ed45ec  /work/AssetKit-0.7.4.tar.gz' | sha256sum --check \
    && git clone --depth 1 --branch v0.7.4 --recurse-submodules --shallow-submodules \
       https://github.com/recp/AssetKit.git /work/source \
    && test "$(git -C /work/source rev-parse HEAD)" = 4f0ec8f2fbca2578d4b927551a51232190892ce2 \
    && test "$(git -C /work/source/deps/cglm rev-parse HEAD)" = b7813d0edb33064d46ba8d30f637c321cdf3cc2c \
    && test "$(git -C /work/source/deps/ds rev-parse HEAD)" = 20faf31bbdc796ad0d791615c5ab65d393bfeee3 \
    && test "$(git -C /work/source/deps/json rev-parse HEAD)" = c69befd5996e29412bc2b705732f6508da19950f \
    && test "$(git -C /work/source/deps/libdeflate rev-parse HEAD)" = b122c8be1d78b19f6d0a6efc5bb79bfcbb30dd51 \
    && test "$(git -C /work/source/deps/xml rev-parse HEAD)" = 4289c02cda9a73a8e11137279a6dc6e9347adee3 \
    && echo 'bd15d2c0f70333f118bcb2d923ed70ca987a3b7bb1d2fc9ee891b9034f1caa14  /work/source/src/io/ply/ascii.c' | sha256sum --check \
    && echo 'ee377012b00624aa65a5f125732c7d9fa6cdd7fa1377df6edfa0022f760bcc09  /work/source/src/io/ply/ply.c' | sha256sum --check
COPY harness.h harness.c replay.c fuzz.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 libstdc++6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
