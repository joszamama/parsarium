FROM --platform=linux/arm64 rust@sha256:f2c004e3d2d8b547e8cf7ffbc29205385f4e71d23e53e4e383065db5e9f822cd AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo fetch --locked --target aarch64-unknown-linux-gnu \
    && find /usr/local/cargo/registry/cache -name sqlite3-parser-0.17.0.crate -exec sha256sum {} + \
       | grep '^fbb44bfd84bfd1bde5ee215dd0b27d10c3c601a1b7cf03a91c7d6f607f2a10f7 ' \
    && echo '88d9b4eb60579c191ec391ca04c16130572d7eedc4a86daa58bf28c6e14c9bcd  /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/sqlite3-parser-0.17.0/LICENSE' | sha256sum --check
RUN rustup component add llvm-tools-preview \
    && cp "$(find /usr/local/rustup/toolchains -path '*/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata' | head -1)" /work/llvm-profdata \
    && cp "$(find /usr/local/rustup/toolchains -path '*/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov' | head -1)" /work/llvm-cov
# The crate's build script compiles its bundled rlemon and generates parse.rs (the
# Lemon LALR tables and grammar actions from src/parser/parse.y) into OUT_DIR.
RUN RUSTFLAGS='-C instrument-coverage -C codegen-units=1' \
    CARGO_TARGET_DIR=/work/target/coverage \
    cargo build --locked --target aarch64-unknown-linux-gnu --release --bin replay \
    && cp /work/target/coverage/aarch64-unknown-linux-gnu/release/replay /work/replay \
    && test "$(find /work/target/coverage -path '*/build/sqlite3-parser-*/out/parse.rs' | wc -l)" = 1
RUN RUSTFLAGS='-Cpasses=sancov-module -Cllvm-args=-sanitizer-coverage-level=4 -Cllvm-args=-sanitizer-coverage-inline-8bit-counters -Cllvm-args=-sanitizer-coverage-pc-table -Cllvm-args=-sanitizer-coverage-trace-compares -Ccodegen-units=1' \
    CARGO_TARGET_DIR=/work/target/fuzz \
    cargo build --locked --target aarch64-unknown-linux-gnu --release --bin fuzzer --features fuzzing \
    && cp /work/target/fuzz/aarch64-unknown-linux-gnu/release/fuzzer /work/fuzzer \
    && nm /work/fuzzer | grep -q '__sancov_gen_'
RUN { rustc --version; cargo --version; /work/llvm-cov --version | head -1; } > /work/toolchain.txt \
    && mkdir -p /work/parser-source /work/generated \
    && cp -a "$(find /usr/local/cargo/registry/src -type d -name sqlite3-parser-0.17.0 | head -1)" /work/parser-source/sqlite3-parser-0.17.0 \
    && cp -a "$(dirname "$(find /work/target/coverage -path '*/build/sqlite3-parser-*/out/parse.rs')")" /work/generated/out \
    && dirname "$(find /work/target/coverage -path '*/build/sqlite3-parser-*/out/parse.rs')" > /work/generated/out-dir.txt

FROM --platform=linux/arm64 debian@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/llvm-cov /work/llvm-profdata /work/
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY --from=build /work/parser-source/sqlite3-parser-0.17.0 /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/sqlite3-parser-0.17.0
COPY --from=build /work/generated /work/generated
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
