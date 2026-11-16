FROM --platform=linux/arm64 rust@sha256:8a4e90c7946b74626488b1446f712c0fe0ed1a596cbd3d871684bc9c5433ae07 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends g++ pkg-config libglib2.0-dev libgdk-pixbuf-2.0-dev libcairo2-dev libpango1.0-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo fetch --locked --target aarch64-unknown-linux-gnu \
    && find /usr/local/cargo/registry/cache -name librsvg-2.63.4.crate -exec sha256sum {} + \
       | grep '^34b84ef0ea0b303ea8cd41858960e572c4820a966c2e4b8e8deb3b67cbe79a95 '
RUN rustup component add llvm-tools-preview \
    && cp "$(find /usr/local/rustup/toolchains -path '*/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata' | head -1)" /work/llvm-profdata \
    && cp "$(find /usr/local/rustup/toolchains -path '*/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov' | head -1)" /work/llvm-cov
RUN RUSTFLAGS='-C instrument-coverage -C codegen-units=1' \
    CARGO_TARGET_DIR=/work/target/coverage \
    cargo build --locked --target aarch64-unknown-linux-gnu --release --bin replay \
    && cp /work/target/coverage/aarch64-unknown-linux-gnu/release/replay /work/replay
RUN RUSTFLAGS='-Cpasses=sancov-module -Cllvm-args=-sanitizer-coverage-level=4 -Cllvm-args=-sanitizer-coverage-inline-8bit-counters -Cllvm-args=-sanitizer-coverage-pc-table -Cllvm-args=-sanitizer-coverage-trace-compares -Ccodegen-units=1' \
    CARGO_TARGET_DIR=/work/target/fuzz \
    cargo build --locked --target aarch64-unknown-linux-gnu --release --bin fuzzer --features fuzzing \
    && cp /work/target/fuzz/aarch64-unknown-linux-gnu/release/fuzzer /work/fuzzer \
    && nm /work/fuzzer | grep -q '__sancov_gen_'
RUN { rustc --version; cargo --version; /work/llvm-cov --version | head -1; } > /work/toolchain.txt \
    && mkdir -p /work/parser-source \
    && cp -a "$(find /usr/local/cargo/registry/src -type d -name librsvg-2.63.4 | head -1)" /work/parser-source/librsvg-2.63.4

FROM --platform=linux/arm64 debian@sha256:a72b4433de1cf7d6bae0c4cee74d0547f58601a643b3375f070c51600d63b6b2
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 librsvg2-2 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/llvm-cov /work/llvm-profdata /work/
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY --from=build /work/parser-source/librsvg-2.63.4 /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/librsvg-2.63.4
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
