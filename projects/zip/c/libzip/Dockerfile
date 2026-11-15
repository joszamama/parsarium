FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 xz-utils zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://libzip.org/download/libzip-1.12.1.tar.xz \
    --output /work/libzip-1.12.1.tar.xz \
    && echo 'c40062022a1963c80573d48f6070792297cecd7c6bffe3aefcac0d8b9bee8913  /work/libzip-1.12.1.tar.xz' | sha256sum --check \
    && tar -xf /work/libzip-1.12.1.tar.xz -C /work
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; cmake --version | head -1; \
         dpkg-query -W -f='${Package}=${Version}\n' clang-21 llvm-21 cmake zlib1g-dev; } \
       > /work/toolchain.txt

FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 zlib1g && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/libzip-1.12.1 /work/libzip-1.12.1
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
