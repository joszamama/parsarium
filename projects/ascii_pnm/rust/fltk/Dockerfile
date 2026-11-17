FROM --platform=linux/arm64 rust@sha256:f2c004e3d2d8b547e8cf7ffbc29205385f4e71d23e53e4e383065db5e9f822cd AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl g++ make pkg-config xz-utils \
    libfontconfig-dev libx11-dev libxcursor-dev libxext-dev libxfixes-dev \
    libxft-dev libxinerama-dev libxrender-dev \
    && rm -rf /var/lib/apt/lists/*
# cfltk 1.5.23 requires CMake >= 3.28; pin Kitware's release instead of relying on apt.
RUN curl --fail --location --retry 3 \
    https://github.com/Kitware/CMake/releases/download/v3.31.10/cmake-3.31.10-linux-aarch64.tar.gz \
    --output /tmp/cmake.tar.gz \
    && echo 'a343c6294f770742904e6a6792e0956b5ff8212abfb63cac99237de2e210fa0f  /tmp/cmake.tar.gz' | sha256sum --check \
    && mkdir /opt/cmake && tar -xzf /tmp/cmake.tar.gz -C /opt/cmake --strip-components=1 && rm /tmp/cmake.tar.gz
# clang must match rustc 1.99.1's LLVM major (23) so C++ and Rust counters share
# one raw profile format and one profiler runtime in the replay binary.
RUN curl --fail --location --retry 3 \
    https://github.com/llvm/llvm-project/releases/download/llvmorg-23.1.3/LLVM-23.1.3-Linux-ARM64.tar.xz \
    --output /tmp/llvm.tar.xz \
    && echo '56d005e339c979a696ed6c244e6472e16f3b1371e48987a07e6145bda7ee0d03  /tmp/llvm.tar.xz' | sha256sum --check \
    && mkdir /opt/llvm && tar -xJf /tmp/llvm.tar.xz -C /opt/llvm --strip-components=1 \
       LLVM-23.1.3-Linux-ARM64/bin/clang-23 LLVM-23.1.3-Linux-ARM64/bin/clang \
       LLVM-23.1.3-Linux-ARM64/bin/clang++ LLVM-23.1.3-Linux-ARM64/lib/clang/23/include \
    && rm /tmp/llvm.tar.xz && /opt/llvm/bin/clang++ --version
WORKDIR /work
COPY Cargo.toml Cargo.lock ./
COPY src ./src
COPY native-cc.sh /work/native-cc.sh
RUN chmod +x /work/native-cc.sh && mkdir /work/bin \
    && ln -s /work/native-cc.sh /work/bin/native-cc && ln -s /work/native-cc.sh /work/bin/native-c++
RUN cargo fetch --locked --target aarch64-unknown-linux-gnu \
    && find /usr/local/cargo/registry/cache -name fltk-1.5.23.crate -exec sha256sum {} + \
       | grep '^78e4a0494d4c6c020514ae1d0b6cc44beddd5f37f0b81bc8e84334652ee15291 ' \
    && find /usr/local/cargo/registry/cache -name fltk-sys-1.5.23.crate -exec sha256sum {} + \
       | grep '^6d9c99e29458923abe3f07b7f8a3bc5b5de3a2c04ad82273fd96402b3666ed06 ' \
    && echo 'd164b0f40ed2ccd32f7c0b91afe978b8a590b0fccb1e242871496c166598e3c2  /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/fltk-sys-1.5.23/cfltk/fltk/src/Fl_PNM_Image.cxx' | sha256sum --check
RUN rustup component add llvm-tools-preview \
    && cp "$(find /usr/local/rustup/toolchains -path '*/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata' | head -1)" /work/llvm-profdata \
    && cp "$(find /usr/local/rustup/toolchains -path '*/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov' | head -1)" /work/llvm-cov
# fltk-sys builds the vendored FLTK through cmake-rs, which takes CC/CXX from
# the environment. native-cc.sh adds instrumentation only to cfltk/FLTK sources.
ENV PATH=/opt/cmake/bin:$PATH \
    CC=/work/bin/native-cc CXX=/work/bin/native-c++ \
    PARSARIUM_REAL_CC=/opt/llvm/bin/clang PARSARIUM_REAL_CXX=/opt/llvm/bin/clang++
RUN PARSARIUM_NATIVE_FLAGS='-fprofile-instr-generate -fcoverage-mapping' \
    RUSTFLAGS='-C instrument-coverage -C codegen-units=1' \
    CARGO_TARGET_DIR=/work/target/coverage \
    cargo build --locked --target aarch64-unknown-linux-gnu --release --bin replay \
    && cp /work/target/coverage/aarch64-unknown-linux-gnu/release/replay /work/replay \
    && ar p "$(find /work/target/coverage -name libfltk_images.a | head -1)" Fl_PNM_Image.cxx.o > /tmp/pnm.o \
    && readelf -S /tmp/pnm.o | grep -q __llvm_covfun \
    && ar p "$(find /work/target/coverage -name libcfltk.a | head -1)" cfl_image.cpp.o > /tmp/shim.o \
    && readelf -S /tmp/shim.o | grep -q __llvm_covfun && rm /tmp/pnm.o /tmp/shim.o
RUN PARSARIUM_NATIVE_FLAGS='-fsanitize-coverage=inline-8bit-counters,pc-table,trace-cmp' \
    RUSTFLAGS='-Cpasses=sancov-module -Cllvm-args=-sanitizer-coverage-level=4 -Cllvm-args=-sanitizer-coverage-inline-8bit-counters -Cllvm-args=-sanitizer-coverage-pc-table -Cllvm-args=-sanitizer-coverage-trace-compares -Ccodegen-units=1' \
    CARGO_TARGET_DIR=/work/target/fuzz \
    cargo build --locked --target aarch64-unknown-linux-gnu --release --bin fuzzer --features fuzzing \
    && cp /work/target/fuzz/aarch64-unknown-linux-gnu/release/fuzzer /work/fuzzer \
    && nm /work/fuzzer | grep -q '__sancov_gen_' \
    && nm -A "$(find /work/target/fuzz -name libfltk_images.a | head -1)" \
       | grep -q 'Fl_PNM_Image.cxx.o:.*U __sanitizer_cov_8bit_counters_init' \
    && nm -A "$(find /work/target/fuzz -name libcfltk.a | head -1)" \
       | grep -q 'cfl_image.cpp.o:.*U __sanitizer_cov_8bit_counters_init'
RUN { rustc --version; cargo --version; /work/llvm-cov --version | head -1; \
      /opt/llvm/bin/clang --version | head -1; cmake --version | head -1; } > /work/toolchain.txt \
    && mkdir -p /work/parser-source \
    && cp -a /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/fltk-1.5.23 /work/parser-source/ \
    && cp -a /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/fltk-sys-1.5.23 /work/parser-source/

FROM --platform=linux/arm64 debian@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libfontconfig1 libstdc++6 libx11-6 libxcursor1 libxext6 libxfixes3 libxft2 \
    libxinerama1 libxrender1 python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/llvm-cov /work/llvm-profdata /work/
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY --from=build /work/parser-source/fltk-1.5.23 /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/fltk-1.5.23
COPY --from=build /work/parser-source/fltk-sys-1.5.23 /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/fltk-sys-1.5.23
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
