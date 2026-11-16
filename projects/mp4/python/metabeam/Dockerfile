FROM --platform=linux/arm64 rust@sha256:8a4e90c7946b74626488b1446f712c0fe0ed1a596cbd3d871684bc9c5433ae07 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/wheels /work/source \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/bc/d6/557913ef8df118bbe28b3aa2825afd2e3e3d559d06caabc681e2b7a8872c/metabeam-0.1.0.tar.gz -o /work/wheels/metabeam-0.1.0.tar.gz \
    && echo '6b003b75189f33782f53d246754c44109aa6f3f874cee79e867078ca7f46e5a8  /work/wheels/metabeam-0.1.0.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/be/1f/265d63c7aa6faf363d4a3f23396f51bc6b4d5c7680a4190ae68dba25dea2/maturin-1.9.6-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.musllinux_1_1_aarch64.whl -o /work/wheels/maturin-1.9.6-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.musllinux_1_1_aarch64.whl \
    && echo 'f5bac167700fbb6f8c8ed1a97b494522554b4432d7578e11403b894b6a91d99f  /work/wheels/maturin-1.9.6-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.musllinux_1_1_aarch64.whl' | sha256sum --check \
    && tar -xzf /work/wheels/metabeam-0.1.0.tar.gz --strip-components=1 -C /work/source \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
COPY fuzz /work/fuzz
ENV PATH=/opt/venv/bin:$PATH
RUN cargo fetch --locked --manifest-path /work/source/python/Cargo.toml \
    && cargo fetch --locked --manifest-path /work/fuzz/Cargo.toml \
    && cd /work/source \
    && RUSTFLAGS='-C instrument-coverage -C codegen-units=1' CARGO_NET_OFFLINE=true /opt/venv/bin/pip install --no-index --no-build-isolation --no-deps . \
    && CARGO_NET_OFFLINE=true cargo build --locked --manifest-path /work/fuzz/Cargo.toml --release \
    && cp /work/fuzz/target/release/fuzzer /work/fuzzer
RUN rustup component add llvm-tools-preview \
    && mkdir /work/llvm-runtime \
    && cp "$(find /usr/local/rustup/toolchains -name llvm-profdata -type f | head -1)" /work/llvm-profdata \
    && cp "$(find /usr/local/rustup/toolchains -name llvm-cov -type f | head -1)" /work/llvm-cov \
    && cp "$(find /usr/local/rustup/toolchains -name 'libLLVM.so.*' -type f | head -1)" /work/llvm-runtime/ \
    && { python3 --version; rustc --version; /opt/venv/bin/pip show metabeam | grep -E '^(Name|Version):'; } > /work/toolchain.txt
FROM --platform=linux/arm64 debian@sha256:a72b4433de1cf7d6bae0c4cee74d0547f58601a643b3375f070c51600d63b6b2
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/work/llvm-runtime
RUN apt-get update -qq && apt-get install -y --no-install-recommends libstdc++6 python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/source /work/source
COPY --from=build /work/llvm-runtime /work/llvm-runtime
COPY --from=build /work/llvm-profdata /work/llvm-cov /work/toolchain.txt /work/fuzzer /work/
RUN ln -s /work/llvm-profdata /usr/local/bin/llvm-profdata \
    && ln -s /work/llvm-cov /usr/local/bin/llvm-cov
COPY adapter.py harness.py fuzz.py merge-native-coverage.py run-control.py run-control.sh target.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
