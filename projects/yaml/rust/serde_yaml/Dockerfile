FROM --platform=linux/arm64 rust@sha256:f2c004e3d2d8b547e8cf7ffbc29205385f4e71d23e53e4e383065db5e9f822cd AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo fetch --locked --target aarch64-unknown-linux-gnu \
    && find /usr/local/cargo/registry/cache -name serde_yaml-0.9.34+deprecated.crate -exec sha256sum {} + \
       | grep '^6a8b1a1a2ebf674015cc02edccce75287f1a0130d394307b36743c2f5d504b47 ' \
    && find /usr/local/cargo/registry/cache -name unsafe-libyaml-0.2.11.crate -exec sha256sum {} + \
       | grep '^673aac59facbab8a9007c7f6108d11f63b603f7cabff99fabf650fea5c32b861 '
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
    && cp -a "$(find /usr/local/cargo/registry/src -type d -name serde_yaml-0.9.34+deprecated | head -1)" /work/parser-source/serde_yaml-0.9.34+deprecated \
    && cp -a "$(find /usr/local/cargo/registry/src -type d -name unsafe-libyaml-0.2.11 | head -1)" /work/parser-source/unsafe-libyaml-0.2.11

FROM --platform=linux/arm64 debian@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/llvm-cov /work/llvm-profdata /work/
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY --from=build /work/parser-source/serde_yaml-0.9.34+deprecated /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/serde_yaml-0.9.34+deprecated
COPY --from=build /work/parser-source/unsafe-libyaml-0.2.11 /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/unsafe-libyaml-0.2.11
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh manifest.json /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
