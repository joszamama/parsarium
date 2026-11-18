FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm make perl python3 \
    libgl-dev libglu1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/JulNadeauCA/libagar/archive/refs/tags/release-1.7.1.tar.gz \
    --output /work/libagar-release-1.7.1.tar.gz \
    && echo '4a376c420a3c7509a15486845dbf0868f300632b00d916d1e18484c3448cab5b  /work/libagar-release-1.7.1.tar.gz' | sha256sum --check \
    && mkdir /work/source \
    && tar -xzf /work/libagar-release-1.7.1.tar.gz -C /work/source --strip-components=1 \
    && rm /work/libagar-release-1.7.1.tar.gz \
    && echo '48243663d25c06c57f8b4d010d7a076476a8953a3a63994827913e3029b0f7eb  /work/source/sg/sg_load_ply.c' | sha256sum --check \
    && echo '276c2661740eb43f20b27a749a9ae01737e1f441c951e87f03c72371187a4501  /work/source/LICENSE' | sha256sum --check
COPY harness.h harness.c replay.c fuzz.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 libgl1 libglu1-mesa libx11-6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
