FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev libglib2.0-dev libxml2-dev llvm make pkg-config python3 xz-utils zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://download.gnome.org/sources/libgsf/1.14/libgsf-1.14.60.tar.xz -o /work/source.tar.xz \
 && echo '83e12c36a099a8a7019bf425e2c24af66eeb2ef5874251e694431a07d9805dae  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 libglib2.0-0t64 libxml2-16 zlib1g \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
