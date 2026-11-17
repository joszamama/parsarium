# C++17 call site over the same tagged resvg 0.50.0 archive, Cargo.lock and Rust 1.92.0 toolchain as projects/svg/c/resvg.
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 ca-certificates clang curl g++ libc6-dev \
    libclang-rt-21-dev libfontconfig1-dev libfreetype-dev llvm pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV CARGO_HOME=/work/cargo-home PATH=/opt/rust/bin:/work/cargo-home/bin:$PATH
# Rust 1.92.0 and Ubuntu LLVM 21 produce compatible LLVM source profiles.
RUN curl --fail --location --retry 3 \
    https://static.rust-lang.org/dist/2025-12-11/rust-1.92.0-aarch64-unknown-linux-gnu.tar.xz \
    -o /work/rust.tar.xz \
    && echo '3e383f8b4fca710d0600d0c1de97b78281672be2cda6575ecbe1c183a12e3822  /work/rust.tar.xz' | sha256sum --check \
    && mkdir /work/rust && tar -xJf /work/rust.tar.xz -C /work/rust --strip-components=1 \
    && /work/rust/install.sh --prefix=/opt/rust --components=rustc,cargo,rust-std-aarch64-unknown-linux-gnu --disable-ldconfig \
    && rm -rf /work/rust /work/rust.tar.xz
# Official resvg 0.50.0 tagged archive; the same archive contains resvg-capi and usvg.
RUN curl --fail --location --retry 3 \
    https://github.com/linebender/resvg/archive/refs/tags/v0.50.0.tar.gz \
    -o /work/source.tar.gz \
    && echo 'ea6629ecaf8ae523aaa42b23217db7fdbed5d4bb070a2574af0d01040195beb1  /work/source.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
    && echo '884bec3fcee36c3c68eb763b9468a0584427b5235de8b7280870bb01f265efed  /work/source/crates/c-api/resvg.h' | sha256sum --check \
    && echo 'fb6a08e06cdd89f59e52065154bac9c8fd3054ddf5a5bca122152f5ae3772a37  /work/source/Cargo.lock' | sha256sum --check \
    && cargo fetch --locked --manifest-path /work/source/Cargo.toml
COPY harness.cpp harness.h replay.cpp fuzz.cpp build.sh rustc-usvg-wrapper.sh /work/
ARG PARSARIUM_BUILD=coverage
RUN chmod +x /work/build.sh /work/rustc-usvg-wrapper.sh && PARSARIUM_BUILD=$PARSARIUM_BUILD /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | grep 'LLVM version'; rustc --version; rustc --version --verbose | grep '^LLVM version'; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 libfontconfig1 libfreetype6 libstdc++6 llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/libresvg.so /work/toolchain.txt /work/
COPY --from=build /work/source/crates/usvg/src/parser /work/source/crates/usvg/src/parser
COPY one-pixel.svg run-control.sh /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
