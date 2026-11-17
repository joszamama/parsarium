# C++17 RAII facade (cpp/include/pdf_oxide/pdf_oxide.hpp) over the C ABI of the tagged pdf_oxide 0.3.78 Rust source.
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 ca-certificates clang curl g++ libc6-dev \
    libclang-rt-21-dev llvm xz-utils \
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
# Official pdf_oxide v0.3.78 tagged archive: Rust engine, C ABI header, C++17 header, and Cargo.lock.
RUN curl --fail --location --retry 3 \
    https://github.com/yfedoseev/pdf_oxide/archive/refs/tags/v0.3.78.tar.gz \
    -o /work/source.tar.gz \
    && echo 'c1f9e4f4737389e3374a058042ebac0b49186604f32663fa7ad3bd016fb764e3  /work/source.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
    && echo 'f823b331c085a696089afa30bbb81ee2b7c2ac7418311dd195d2eef4f2a87420  /work/source/cpp/include/pdf_oxide/pdf_oxide.hpp' | sha256sum --check \
    && echo '95d83bb4acce1461cae72bdaf4ce149fecc9653d029b8861bfb61d2eb3a502ef  /work/source/include/pdf_oxide_c/pdf_oxide.h' | sha256sum --check \
    && echo 'f68da643f5719de451e00253fcf46a4f47eead5a241f97baed080cb632ae42f6  /work/source/Cargo.lock' | sha256sum --check \
    && cargo fetch --locked --manifest-path /work/source/Cargo.toml
COPY harness.cpp harness.h replay.cpp fuzz.cpp build.sh rustc-pdf-oxide-wrapper.sh /work/
ARG PARSARIUM_BUILD=coverage
RUN chmod +x /work/build.sh /work/rustc-pdf-oxide-wrapper.sh && PARSARIUM_BUILD=$PARSARIUM_BUILD /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | grep 'LLVM version'; rustc --version; rustc --version --verbose | grep '^LLVM version'; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 libstdc++6 llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/libpdf_oxide.so /work/toolchain.txt /work/
COPY --from=build /work/source/src /work/source/src
COPY two-page.pdf run-control.sh /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
