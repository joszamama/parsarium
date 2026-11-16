FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/google/wuffs/archive/refs/tags/v0.3.6.tar.gz -o /work/wuffs.tar.gz \
    && echo 'e669099e0f67123efa1d24f88f4ec26ef9875bc7d8957e0d4d9df9803ff5c039  /work/wuffs.tar.gz' | sha256sum --check \
    && tar -xf /work/wuffs.tar.gz -C /work \
    && mv /work/wuffs-0.3.6 /work/wuffs-src \
    && echo '8295f8cc851c6bc8bf6bd1720623372c6983a8c6dbd2875c5aace259d4b3c5d3  /work/wuffs-src/release/c/wuffs-v0.3.c' | sha256sum --check
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/wuffs-src /work/wuffs-src
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
