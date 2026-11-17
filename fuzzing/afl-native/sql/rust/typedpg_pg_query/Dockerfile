# AFL++ feedback from the typedpg_pg_query 0.7.3 Rust path and the libpg_query grammar, scanner and
# raw_parser entry it calls. Hand-written (built by build.py); scripts/build_afl_rust.py would overwrite it.
FROM --platform=linux/arm64 rust@sha256:f2c004e3d2d8b547e8cf7ffbc29205385f4e71d23e53e4e383065db5e9f822cd AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl g++ llvm-dev make python3 xz-utils \
    && rm -rf /var/lib/apt/lists/*
# Debian's clang 14 cannot compile libpg_query's src_port_pg_popcount_aarch64.c (SVE
# intrinsics), so the C objects use the same pinned clang 23.1.3 as the base project.
RUN curl --fail --location --retry 3 \
    https://github.com/llvm/llvm-project/releases/download/llvmorg-23.1.3/LLVM-23.1.3-Linux-ARM64.tar.xz \
    --output /tmp/llvm.tar.xz \
    && echo '56d005e339c979a696ed6c244e6472e16f3b1371e48987a07e6145bda7ee0d03  /tmp/llvm.tar.xz' | sha256sum --check \
    && mkdir /opt/llvm && tar -xJf /tmp/llvm.tar.xz -C /opt/llvm --strip-components=1 \
       LLVM-23.1.3-Linux-ARM64/bin/clang-23 LLVM-23.1.3-Linux-ARM64/bin/clang \
       LLVM-23.1.3-Linux-ARM64/lib/clang/23/include \
    && rm /tmp/llvm.tar.xz && /opt/llvm/bin/clang --version
RUN cargo install cargo-afl --version 0.18.2 --locked
WORKDIR /work
COPY fuzzing/afl-native/sql/rust/typedpg_pg_query/Cargo.toml fuzzing/afl-native/sql/rust/typedpg_pg_query/Cargo.lock /work/
COPY projects/sql/rust/typedpg_pg_query/src /work/src
COPY fuzzing/afl-native/sql/rust/typedpg_pg_query/afl_fuzzer.rs /work/src/bin/afl_fuzzer.rs
COPY fuzzing/afl-native/sql/rust/typedpg_pg_query/c-allowlist.txt /work/c-allowlist.txt
RUN cargo fetch --locked --target aarch64-unknown-linux-gnu \
    && find /usr/local/cargo/registry/cache -name typedpg_pg_query-0.7.3.crate -exec sha256sum {} + \
       | grep '^d68e4f3097f7b7b552e7940175ee9be617997aebc99bc6c2a20070fc63a05320 '
RUN cargo afl config --build --force
# cargo-afl instruments the Rust crates with SanitizerCoverage trace-pc-guard and links AFL++'s
# compiler runtime. clang 23 gives the libpg_query parser objects (gram.c, scan.c, parser.c only,
# via the allowlist) the same callbacks, so both feed one AFL++ map.
RUN CC_aarch64_unknown_linux_gnu=/opt/llvm/bin/clang \
    CFLAGS_aarch64_unknown_linux_gnu='-fsanitize-coverage=trace-pc-guard,no-prune,trace-cmp -fsanitize-coverage-allowlist=/work/c-allowlist.txt' \
    CARGO_TARGET_DIR=/work/target/afl \
    cargo afl build --locked --target aarch64-unknown-linux-gnu --release --bin afl_fuzzer --bin replay \
    && cp /work/target/afl/aarch64-unknown-linux-gnu/release/afl_fuzzer /work/afl_fuzzer \
    && cp /work/target/afl/aarch64-unknown-linux-gnu/release/replay /work/replay \
    && out="$(dirname "$(find /work/target/afl -path '*/build/typedpg_pg_query-*/out/version.rs' | head -1)")" \
    && for object in $(find "$out" -name '*.o'); do \
         if nm "$object" | grep -q '__sanitizer_cov_trace_pc_guard'; then basename "$object" | sed 's/^[0-9a-f]*-//'; fi; \
       done | sort > /work/afl-instrumented-objects.txt \
    && printf '%s\n' src_backend_parser_gram.o src_backend_parser_parser.o src_backend_parser_scan.o > /work/afl-expected-objects.txt \
    && cmp /work/afl-instrumented-objects.txt /work/afl-expected-objects.txt
# Same Rust instrumentation with uninstrumented C, so build.py can attribute the extra tuples
# to the native parser.
RUN CC_aarch64_unknown_linux_gnu=/opt/llvm/bin/clang CARGO_TARGET_DIR=/work/target/afl-rust-only \
    cargo afl build --locked --target aarch64-unknown-linux-gnu --release --bin afl_fuzzer \
    && cp /work/target/afl-rust-only/aarch64-unknown-linux-gnu/release/afl_fuzzer /work/afl_fuzzer_rust_only
RUN { rustc --version; cargo install --list | grep "^cargo-afl "; /opt/llvm/bin/clang --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /work/afl_fuzzer /work/afl_fuzzer_rust_only /work/replay /work/toolchain.txt /work/afl-instrumented-objects.txt /work/
ENTRYPOINT ["/work/afl_fuzzer"]
