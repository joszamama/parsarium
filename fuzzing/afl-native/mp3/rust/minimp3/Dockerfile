# Native AFL++ overlay: only the vendored minimp3 C decoder is instrumented; Rust code is not.
FROM --platform=linux/arm64 parsarium/mp3-rust-minimp3:local
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.04c-4 \
    && rm -rf /var/lib/apt/lists/*
COPY afl-allowlist.txt /work/allowlist
RUN AFL_LLVM_ALLOWLIST=/work/allowlist AFL_LLVM_INSTRUMENT=CLASSIC CC=afl-clang-fast \
    RUSTFLAGS='-C link-arg=/usr/lib/afl/afl-compiler-rt.o -C link-arg=-lc -C link-arg=-ldl -C link-arg=-lpthread' \
    CARGO_TARGET_DIR=/work/target/afl \
    cargo build --locked --offline --target aarch64-unknown-linux-gnu --release --bin afl_target \
    && cp /work/target/afl/aarch64-unknown-linux-gnu/release/afl_target /work/afl-target \
    && nm "$(find /work/target/afl -name libminimp3.a)" | grep -q ' U __afl_area_ptr$'
ENTRYPOINT ["/work/afl-target"]
