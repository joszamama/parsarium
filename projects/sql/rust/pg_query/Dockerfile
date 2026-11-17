FROM --platform=linux/arm64 rust@sha256:f2c004e3d2d8b547e8cf7ffbc29205385f4e71d23e53e4e383065db5e9f822cd AS build
ENV DEBIAN_FRONTEND=noninteractive
# libclang-dev serves bindgen in pg_query's build script; protoc is deliberately absent, so
# the crate uses its shipped src/protobuf.rs instead of regenerating it.
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl g++ libclang-dev xz-utils \
    && rm -rf /var/lib/apt/lists/*
# clang must match rustc 1.99.1's LLVM major (23) so the libpg_query C counters and the
# Rust counters share one raw profile format and one profiler runtime in the replay binary.
RUN curl --fail --location --retry 3 \
    https://github.com/llvm/llvm-project/releases/download/llvmorg-23.1.3/LLVM-23.1.3-Linux-ARM64.tar.xz \
    --output /tmp/llvm.tar.xz \
    && echo '56d005e339c979a696ed6c244e6472e16f3b1371e48987a07e6145bda7ee0d03  /tmp/llvm.tar.xz' | sha256sum --check \
    && mkdir /opt/llvm && tar -xJf /tmp/llvm.tar.xz -C /opt/llvm --strip-components=1 \
       LLVM-23.1.3-Linux-ARM64/bin/clang-23 LLVM-23.1.3-Linux-ARM64/bin/clang \
       LLVM-23.1.3-Linux-ARM64/lib/clang/23/include \
    && rm /tmp/llvm.tar.xz && /opt/llvm/bin/clang --version
WORKDIR /work
COPY Cargo.toml Cargo.lock ./
COPY src ./src
ENV PG_QUERY_SRC=/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/pg_query-18.1.0
# The bison/flex outputs carry #line directives to gram.y and scan.l, which the crate does not
# ship; they are removed (after the crate checksum is verified) so coverage is attributed to the
# pinned C files, as in the C libpg_query path. No other source line changes.
RUN cargo fetch --locked --target aarch64-unknown-linux-gnu \
    && find /usr/local/cargo/registry/cache -name pg_query-18.1.0.crate -exec sha256sum {} + \
       | grep '^457bfe74085c505ecaf5468416450969e2e52a66d26bc1a4b2f6944a2daee73f ' \
    && grep -qx 'license = "MIT"' "$PG_QUERY_SRC/Cargo.toml" \
    && sed -i '/^#line /d' "$PG_QUERY_SRC/libpg_query/src/postgres/src_backend_parser_gram.c" \
       "$PG_QUERY_SRC/libpg_query/src/postgres/src_backend_parser_scan.c" \
    && ! grep -q '^#line ' "$PG_QUERY_SRC/libpg_query/src/postgres/src_backend_parser_gram.c"
RUN rustup component add llvm-tools-preview \
    && cp "$(find /usr/local/rustup/toolchains -path '*/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata' | head -1)" /work/llvm-profdata \
    && cp "$(find /usr/local/rustup/toolchains -path '*/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov' | head -1)" /work/llvm-cov
# The cc crate compiles libpg_query from the build script's OUT_DIR copy; CC/CFLAGS put that C
# under clang 23 source coverage. run-control.sh maps OUT_DIR back to the crate's libpg_query.
RUN CC_aarch64_unknown_linux_gnu=/opt/llvm/bin/clang \
    CFLAGS_aarch64_unknown_linux_gnu='-fprofile-instr-generate -fcoverage-mapping' \
    RUSTFLAGS='-C instrument-coverage -C codegen-units=1' \
    CARGO_TARGET_DIR=/work/target/coverage \
    cargo build --locked --target aarch64-unknown-linux-gnu --release --bin replay \
    && cp /work/target/coverage/aarch64-unknown-linux-gnu/release/replay /work/replay \
    && out="$(dirname "$(find /work/target/coverage -path '*/build/pg_query-*/out/pg_query.h' | head -1)")" \
    && test -n "$out" && echo "$out" > /work/pg-query-out-dir.txt \
    && readelf -S "$(find "$out" -name '*src_backend_parser_gram.o' | head -1)" | grep -q __llvm_covfun
RUN CC_aarch64_unknown_linux_gnu=/opt/llvm/bin/clang \
    CFLAGS_aarch64_unknown_linux_gnu='-fsanitize-coverage=inline-8bit-counters,pc-table,trace-cmp' \
    RUSTFLAGS='-Cpasses=sancov-module -Cllvm-args=-sanitizer-coverage-level=4 -Cllvm-args=-sanitizer-coverage-inline-8bit-counters -Cllvm-args=-sanitizer-coverage-pc-table -Cllvm-args=-sanitizer-coverage-trace-compares -Ccodegen-units=1' \
    CARGO_TARGET_DIR=/work/target/fuzz \
    cargo build --locked --target aarch64-unknown-linux-gnu --release --bin fuzzer --features fuzzing \
    && cp /work/target/fuzz/aarch64-unknown-linux-gnu/release/fuzzer /work/fuzzer \
    && nm /work/fuzzer | grep -q '__sancov_gen_'
RUN { rustc --version; cargo --version; /work/llvm-cov --version | head -1; \
      /opt/llvm/bin/clang --version | head -1; } > /work/toolchain.txt \
    && mkdir -p /work/parser-source \
    && cp -a "$PG_QUERY_SRC" /work/parser-source/pg_query-18.1.0

FROM --platform=linux/arm64 debian@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/llvm-cov /work/llvm-profdata /work/pg-query-out-dir.txt /work/
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY --from=build /work/parser-source/pg_query-18.1.0 /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/pg_query-18.1.0
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
