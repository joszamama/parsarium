# AFL++ feedback from the fltk 1.5.23 Rust path and the FLTK 1.4.5 C++ PNM loader it calls.
# Hand-written (built by build.py); scripts/build_afl_rust.py --all would overwrite it.
FROM --platform=linux/arm64 rust@sha256:f2c004e3d2d8b547e8cf7ffbc29205385f4e71d23e53e4e383065db5e9f822cd AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl g++ llvm-dev make pkg-config python3 \
    libfontconfig-dev libx11-dev libxcursor-dev libxext-dev libxfixes-dev \
    libxft-dev libxinerama-dev libxrender-dev \
    && rm -rf /var/lib/apt/lists/*
RUN curl --fail --location --retry 3 \
    https://github.com/Kitware/CMake/releases/download/v3.31.10/cmake-3.31.10-linux-aarch64.tar.gz \
    --output /tmp/cmake.tar.gz \
    && echo 'a343c6294f770742904e6a6792e0956b5ff8212abfb63cac99237de2e210fa0f  /tmp/cmake.tar.gz' | sha256sum --check \
    && mkdir /opt/cmake && tar -xzf /tmp/cmake.tar.gz -C /opt/cmake --strip-components=1 && rm /tmp/cmake.tar.gz
RUN cargo install cargo-afl --version 0.18.2 --locked
WORKDIR /work
COPY fuzzing/afl-native/ascii_pnm/rust/fltk/Cargo.toml fuzzing/afl-native/ascii_pnm/rust/fltk/Cargo.lock /work/
COPY projects/ascii_pnm/rust/fltk/src /work/src
COPY fuzzing/afl-native/ascii_pnm/rust/fltk/afl_fuzzer.rs /work/src/bin/afl_fuzzer.rs
COPY projects/ascii_pnm/rust/fltk/native-cc.sh /work/native-cc.sh
RUN chmod +x /work/native-cc.sh && mkdir /work/bin \
    && ln -s /work/native-cc.sh /work/bin/native-cc && ln -s /work/native-cc.sh /work/bin/native-c++
RUN cargo fetch --locked --target aarch64-unknown-linux-gnu \
    && find /usr/local/cargo/registry/cache -name fltk-1.5.23.crate -exec sha256sum {} + \
       | grep '^78e4a0494d4c6c020514ae1d0b6cc44beddd5f37f0b81bc8e84334652ee15291 ' \
    && find /usr/local/cargo/registry/cache -name fltk-sys-1.5.23.crate -exec sha256sum {} + \
       | grep '^6d9c99e29458923abe3f07b7f8a3bc5b5de3a2c04ad82273fd96402b3666ed06 '
RUN cargo afl config --build --force
# cargo-afl instruments Rust with SanitizerCoverage trace-pc-guard and links
# AFL++'s afl-compiler-rt. The FLTK/cfltk C++ objects get the same callbacks
# from clang, so both languages feed one AFL++ map.
ENV PATH=/opt/cmake/bin:$PATH \
    CC=/work/bin/native-cc CXX=/work/bin/native-c++ \
    PARSARIUM_REAL_CC=clang PARSARIUM_REAL_CXX=clang++
RUN PARSARIUM_NATIVE_FLAGS='-fsanitize-coverage=trace-pc-guard,no-prune,trace-cmp' \
    CARGO_TARGET_DIR=/work/target/afl \
    cargo afl build --locked --target aarch64-unknown-linux-gnu --release --bin afl_fuzzer --bin replay \
    && cp /work/target/afl/aarch64-unknown-linux-gnu/release/afl_fuzzer /work/afl_fuzzer \
    && cp /work/target/afl/aarch64-unknown-linux-gnu/release/replay /work/replay \
    && nm -A "$(find /work/target/afl -name libfltk_images.a | head -1)" \
       | grep -q 'Fl_PNM_Image.cxx.o:.*U __sanitizer_cov_trace_pc_guard' \
    && nm -A "$(find /work/target/afl -name libcfltk.a | head -1)" \
       | grep -q 'cfl_image.cpp.o:.*U __sanitizer_cov_trace_pc_guard'
# Same Rust instrumentation with uninstrumented FLTK, so build.py can attribute
# the control's extra AFL++ tuples to the native code.
RUN PARSARIUM_NATIVE_FLAGS='' CARGO_TARGET_DIR=/work/target/afl-rust-only \
    cargo afl build --locked --target aarch64-unknown-linux-gnu --release --bin afl_fuzzer \
    && cp /work/target/afl-rust-only/aarch64-unknown-linux-gnu/release/afl_fuzzer /work/afl_fuzzer_rust_only \
    && ! nm -A "$(find /work/target/afl-rust-only -name libfltk_images.a | head -1)" \
       | grep -q 'Fl_PNM_Image.cxx.o:.*U __sanitizer_cov_trace_pc_guard'
RUN { rustc --version; cargo install --list | grep "^cargo-afl "; clang --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 \
    libfontconfig1 libstdc++6 libx11-6 libxcursor1 libxext6 libxfixes3 libxft2 \
    libxinerama1 libxrender1 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /work/afl_fuzzer /work/afl_fuzzer_rust_only /work/replay /work/toolchain.txt /work/
ENTRYPOINT ["/work/afl_fuzzer"]
