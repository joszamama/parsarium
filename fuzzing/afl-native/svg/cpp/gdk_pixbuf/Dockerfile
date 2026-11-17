# AFL++ overlay for projects/svg/c/gdk_pixbuf: same pinned sources, librsvg built with pcguard edges
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 ca-certificates clang curl gcc libc6-dev libcairo2-dev libclang-rt-21-dev libcurl4-openssl-dev libfreetype-dev libglib2.0-dev libharfbuzz-dev libpango1.0-dev libssl-dev libxml2-dev llvm meson ninja-build pkg-config python3 xz-utils zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV CARGO_HOME=/work/cargo-home PATH=/opt/rust/bin:/work/cargo-home/bin:$PATH LD_LIBRARY_PATH=/work/install/lib
# Rust 1.92.0 is librsvg 2.63.4's MSRV and uses LLVM 21, matching Ubuntu's clang/llvm-cov 21.
RUN curl --fail --location --retry 3 https://static.rust-lang.org/dist/2025-12-11/rust-1.92.0-aarch64-unknown-linux-gnu.tar.xz -o /work/rust.tar.xz \
 && echo '3e383f8b4fca710d0600d0c1de97b78281672be2cda6575ecbe1c183a12e3822  /work/rust.tar.xz' | sha256sum --check \
 && mkdir /work/rust && tar -xJf /work/rust.tar.xz -C /work/rust --strip-components=1 \
 && /work/rust/install.sh --prefix=/opt/rust --components=rustc,cargo,rust-std-aarch64-unknown-linux-gnu --disable-ldconfig \
 && rm -rf /work/rust /work/rust.tar.xz
RUN cargo install cargo-c --version 0.10.21 --locked
RUN curl --fail --location --retry 3 https://download.gnome.org/sources/gdk-pixbuf/2.44/gdk-pixbuf-2.44.8.tar.xz -o /work/source.tar.xz \
 && echo '919f529512961a12e81cd4b4b466a48c3933469e7f9a310c6513cd4fb252ba3c  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1 \
 && curl --fail --location --retry 3 https://download.gnome.org/sources/librsvg/2.63/librsvg-2.63.4.tar.xz -o /work/librsvg.tar.xz \
 && echo '31f07d9350dad3f8964fd613c31309ac160fdef13dfac59df6fd082de78d6e8f  /work/librsvg.tar.xz' | sha256sum --check \
 && mkdir /work/librsvg && tar -xJf /work/librsvg.tar.xz -C /work/librsvg --strip-components=1 \
 && cargo fetch --locked --manifest-path /work/librsvg/Cargo.toml
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && PARSARIUM_BUILD=afl /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | grep 'LLVM version'; rustc --version; rustc --version --verbose | grep '^LLVM version'; cargo cbuild --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 libcairo2-dev libglib2.0-dev libpango1.0-dev libxml2-dev llvm python3 libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV LD_LIBRARY_PATH=/work/install/lib
# Preload the Rust SVG loader so librsvg's pcguard edges register before the fork server starts.
ENV AFL_PRELOAD=/work/install/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader_svg.so
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/librsvg /work/librsvg
COPY --from=build /work/install /work/install
COPY --from=build /work/toolchain.txt /work/toolchain.txt
ENTRYPOINT ["/work/fuzzer"]
