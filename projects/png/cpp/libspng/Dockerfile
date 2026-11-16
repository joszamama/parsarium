FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm python3 zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/randy408/libspng/archive/refs/tags/v0.7.4.tar.gz -o /work/libspng.tar.gz \
    && echo '47ec02be6c0a6323044600a9221b049f63e1953faf816903e7383d4dc4234487  /work/libspng.tar.gz' | sha256sum --check \
    && tar -xf /work/libspng.tar.gz -C /work \
    && mv /work/libspng-0.7.4 /work/libspng-src \
    && echo '59243c1ca05956f124c7debef763b707378b52e4dbfeaf17e6192917dd8c8dc2  /work/libspng-src/spng/spng.c' | sha256sum --check
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 zlib1g && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/libspng-src /work/libspng-src
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
