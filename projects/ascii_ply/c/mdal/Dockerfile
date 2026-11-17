FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/lutraconsulting/MDAL/archive/refs/tags/release-1.3.3.tar.gz \
    --output /work/MDAL-release-1.3.3.tar.gz \
    && echo 'aeff0d532653c042c24bafe250409052fcb0bc6b2bab09f6470c858a3e079b2f  /work/MDAL-release-1.3.3.tar.gz' | sha256sum --check \
    && mkdir /work/MDAL-release-1.3.3 \
    && tar -xf /work/MDAL-release-1.3.3.tar.gz -C /work/MDAL-release-1.3.3 --strip-components=1 \
    && echo 'd81558aee3cf369f62e9b0d9b78099bd89ced5954f424d248eb9d35ad60a62d2  /work/MDAL-release-1.3.3/mdal/frmts/mdal_ply.cpp' | sha256sum --check
COPY harness.h mdal_c_compat.h harness.c replay.c fuzz.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 libstdc++6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/MDAL-release-1.3.3 /work/MDAL-release-1.3.3
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
