FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm make pkg-config python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-1.0.10.tar.gz \
    --output /work/libmicrohttpd-1.0.10.tar.gz \
    && echo '04bfe8ef75db7d629a33de767599765cecadc56274a39822d5d081030d577685  /work/libmicrohttpd-1.0.10.tar.gz' | sha256sum --check \
    && mkdir /work/source \
    && tar -xzf /work/libmicrohttpd-1.0.10.tar.gz -C /work/source --strip-components=1 \
    && echo 'b254988f28fd39870384988025cd9196bb6ff7ea38466d70a0dc2f421aafd66e  /work/source/src/microhttpd/connection.c' | sha256sum --check \
    && echo '18429c414ce9572981900d73250cbde57903a5b7e1a314e8ab43389261e63124  /work/source/src/microhttpd/mhd_str.c' | sha256sum --check
COPY harness.h harness.cpp replay.cpp fuzz.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
