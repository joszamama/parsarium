FROM --platform=linux/arm64 rust@sha256:b78cfbe4c0fd96b8a06b259092f1f412cb3ad3c5aed89d188bc40a1b8637f8f6 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV PATH=/opt/venv/bin:$PATH
# The sdist's rust-toolchain file says "stable"; the image's pinned 1.99.1 toolchain is used instead.
ENV RUSTUP_TOOLCHAIN=1.99.1
# A fixed CARGO_HOME gives the sqlparser crate a stable source path for coverage and AFL++ features.
ENV CARGO_HOME=/work/cargo
COPY build-requirements.lock ./
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# sqloxide 0.61.1 sdist: src/lib.rs (pyo3 binding) and Cargo.lock pinning sqlparser 0.61.0, pyo3 and pythonize by checksum.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/78/b4/20b2d9c217f66ea23c12052db2c47f88e968940706758e5ab15765eb78e8/sqloxide-0.61.1.tar.gz -o /work/sqloxide.tar.gz \
    && echo '2ff1d48e6b59f2870e5e37d391eed82c126db001c30cd92383ea048cc69a5576  /work/sqloxide.tar.gz' | sha256sum --check \
    && mkdir /work/sqloxide-source && tar -xzf /work/sqloxide.tar.gz -C /work/sqloxide-source --strip-components=1 \
    && cd /work/sqloxide-source \
    && printf '%s\n' \
       'e0cb53c8dbf8048278fe3161168405898f4cf269450068b32f2862ef62678a36  src/lib.rs' \
       '4887ed0505457d387e7f7effda202be2374379f4fecf491e54ca67f59a77640b  LICENSE' \
       | sha256sum --check \
    && grep -qx 'MIT License' LICENSE \
    && grep -A1 '^name = "sqlparser"$' Cargo.lock | grep -qx 'version = "0.61.0"'
RUN rustup component add llvm-tools-preview \
    && cd /work/sqloxide-source \
    && RUSTFLAGS='-C instrument-coverage -C codegen-units=1' CARGO_PROFILE_RELEASE_DEBUG=1 CARGO_PROFILE_RELEASE_LTO=off \
       MATURIN_PEP517_ARGS='--locked' \
       /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/sqloxide-source -w /work/wheels \
    && test -f /work/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/sqlparser-0.61.0/src/parser/mod.rs \
    && grep -q 'Apache License' /work/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/sqlparser-0.61.0/LICENSE.TXT
RUN /opt/venv/bin/pip install --no-index --no-deps /work/wheels/sqloxide-*.whl \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import sqloxide; print(sqloxide.parse_sql("SELECT 1", dialect="generic")[0].keys())'
RUN { python3 --version; rustc --version; /opt/venv/bin/pip show sqloxide maturin | grep -E '^(Name|Version):'; echo 'sqlparser 0.61.0 (crates.io, pinned by the sdist Cargo.lock)'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-sqloxide-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/sqloxide-source/src /work/sqloxide-source/src
COPY --from=build /work/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/sqlparser-0.61.0/src /work/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/sqlparser-0.61.0/src
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov /usr/local/bin/llvm-cov
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata /usr/local/bin/llvm-profdata
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY harness.py replay.py fuzz.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
