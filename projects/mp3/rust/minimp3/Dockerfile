FROM --platform=linux/arm64 rust@sha256:f2c004e3d2d8b547e8cf7ffbc29205385f4e71d23e53e4e383065db5e9f822cd
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    clang=1:14.0-55.7~deb12u1 llvm=1:14.0-55.7~deb12u1 \
    libclang-rt-14-dev=1:14.0.6-12 python3=3.11.2-1+b1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY Cargo.toml Cargo.lock ./
COPY src ./src
ENV REGISTRY=/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f
RUN cargo fetch --locked --target aarch64-unknown-linux-gnu \
    && find /usr/local/cargo/registry/cache -name minimp3-0.6.1.crate -exec sha256sum {} + \
       | grep '^82acfc4ecae15a73fc88d4f5f6ba6e2eece7ed980f1a63fccd1ae374c2a0b7c5 ' \
    && find /usr/local/cargo/registry/cache -name minimp3-sys-0.6.0.crate -exec sha256sum {} + \
       | grep '^aa16a1fbac806d94e230e0a6b9b5a137d051897a188944cf07645da4b73a9fae ' \
    && echo "5fb296a790734772b65a5514438cc06d14f24e539c13475ff2a7f737681c82c0  $REGISTRY/minimp3-sys-0.6.0/minimp3/minimp3.h" \
       | sha256sum --check
RUN rustup component add llvm-tools-preview \
    && ln -s "$(find /usr/local/rustup/toolchains -path '*/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata' | head -1)" /work/rust-llvm-profdata \
    && ln -s "$(find /usr/local/rustup/toolchains -path '*/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov' | head -1)" /work/rust-llvm-cov
# Rust binding lines: rustc source coverage; the minimp3 C decoder is built by clang without instrumentation.
RUN CC=clang RUSTFLAGS='-C instrument-coverage -C codegen-units=1' \
    CARGO_TARGET_DIR=/work/target/rust-coverage \
    cargo build --locked --offline --target aarch64-unknown-linux-gnu --release --bin replay \
    && cp /work/target/rust-coverage/aarch64-unknown-linux-gnu/release/replay /work/replay
# Native decoder lines: only minimp3.c/minimp3.h carry Clang source coverage; Rust code is uninstrumented.
RUN PROFILE_RT="$(clang -print-runtime-dir)/libclang_rt.profile-aarch64.a" \
    && test -f "$PROFILE_RT" \
    && CC=clang CFLAGS='-fprofile-instr-generate -fcoverage-mapping' \
    RUSTFLAGS="-C link-arg=-Wl,-u,__llvm_profile_runtime -C link-arg=$PROFILE_RT -C link-arg=-lc" \
    CARGO_TARGET_DIR=/work/target/native-coverage \
    cargo build --locked --offline --target aarch64-unknown-linux-gnu --release --bin replay \
    && cp /work/target/native-coverage/aarch64-unknown-linux-gnu/release/replay /work/native-replay \
    && nm /work/native-replay | grep -q ' __llvm_profile_write_file$'
RUN CC=clang CXX=clang++ CFLAGS='-fsanitize=fuzzer-no-link' \
    RUSTFLAGS='-Cpasses=sancov-module -Cllvm-args=-sanitizer-coverage-level=4 -Cllvm-args=-sanitizer-coverage-inline-8bit-counters -Cllvm-args=-sanitizer-coverage-pc-table -Cllvm-args=-sanitizer-coverage-trace-compares -Ccodegen-units=1' \
    CARGO_TARGET_DIR=/work/target/fuzz \
    cargo build --locked --offline --target aarch64-unknown-linux-gnu --release --bin fuzzer --features fuzzing \
    && cp /work/target/fuzz/aarch64-unknown-linux-gnu/release/fuzzer /work/fuzzer \
    && nm /work/fuzzer | grep -q '__sancov_gen_'
RUN { rustc --version; cargo --version; clang --version | head -1; /work/rust-llvm-cov --version | grep -m1 'LLVM version'; } > /work/toolchain.txt
COPY report.py ./
ENTRYPOINT ["python3", "/work/report.py"]
