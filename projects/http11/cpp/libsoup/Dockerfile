FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev libglib2.0-dev libnghttp2-dev libpsl-dev \
    libsqlite3-dev llvm meson ninja-build pkg-config python3 xz-utils zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://download.gnome.org/sources/libsoup/3.8/libsoup-3.8.1.tar.xz \
    --output /work/libsoup-3.8.1.tar.xz \
    && echo '5013dcef9136f6f861e6529fca578af50c1f52a39219027fb5aff652d1371a04  /work/libsoup-3.8.1.tar.xz' | sha256sum --check \
    && mkdir /work/source \
    && tar -xJf /work/libsoup-3.8.1.tar.xz -C /work/source --strip-components=1 \
    && echo '80b09f3ef065afb98f512c5dd10e44081f8fa1516c802468e0e62dbf3337657e  /work/source/libsoup/soup-headers.c' | sha256sum --check
COPY harness.h harness.cpp replay.cpp fuzz.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libglib2.0-0t64 libnghttp2-14 libpsl5t64 libsqlite3-0 libstdc++6 llvm python3 zlib1g \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
