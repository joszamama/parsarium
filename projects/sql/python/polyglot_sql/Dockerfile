FROM --platform=linux/arm64 rust@sha256:b78cfbe4c0fd96b8a06b259092f1f412cb3ad3c5aed89d188bc40a1b8637f8f6 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV PATH=/opt/venv/bin:$PATH
ENV RUSTUP_TOOLCHAIN=1.99.1
ENV CARGO_HOME=/work/cargo
COPY build-requirements.lock ./
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# polyglot-sql 0.14.1 sdist: the polyglot-sql parser crate (crates/polyglot-sql, same src/ as the crates.io
# polyglot-sql 0.14.1 crate), its pyo3 binding (crates/polyglot-sql-python) and a Cargo.lock pinning
# pyo3 and pythonize by checksum. The sdist ships no licence file; pyproject.toml and the workspace
# Cargo.toml declare MIT.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/0d/6f/49d1a02cc143a2f23dc3b0a835682e8024139e3f2832529fc1e4d2df82a8/polyglot_sql-0.14.1.tar.gz -o /work/polyglot.tar.gz \
    && echo '7f39f90c307336177576f7ce3a83a53567c0a9578b7ff3cbf04d76546932b0ab  /work/polyglot.tar.gz' | sha256sum --check \
    && mkdir /work/polyglot-source && tar -xzf /work/polyglot.tar.gz -C /work/polyglot-source --strip-components=1 \
    && cd /work/polyglot-source \
    && printf '%s\n' \
       '3631cbf89f2c830cafd4fc047696df0440cb36ccba5d29b67369a85f957989af  crates/polyglot-sql/src/parser.rs' \
       'c74729bab211efdbcd550fc045e334bcbe9a00878bd21198dee0533f74a5ee7f  crates/polyglot-sql-python/src/parse.rs' \
       'fdce31e525bfa9431e699ec1381a7f9f8f8c04d9a03fb5ce8c92ace9bea53b34  Cargo.lock' \
       | sha256sum --check \
    && grep -qx 'license = { text = "MIT" }' pyproject.toml \
    && grep -qx 'license = "MIT"' Cargo.toml \
    && grep -qx 'version = "0.14.1"' Cargo.toml
# The sdist Cargo.lock also lists crates of workspace members the sdist does not ship (FFI/WASM
# tooling), so cargo prunes them on the first fetch. The pruned lock must be a strict subset of the
# shipped one (same names, versions and checksums); the build then runs with --locked against it.
RUN cd /work/polyglot-source && cp Cargo.lock /work/Cargo.lock.sdist && cargo fetch \
    && python3 -c 'import tomllib; old = {(p["name"], p["version"], p.get("checksum")) for p in tomllib.load(open("/work/Cargo.lock.sdist", "rb"))["package"]}; new = {(p["name"], p["version"], p.get("checksum")) for p in tomllib.load(open("Cargo.lock", "rb"))["package"]}; assert new <= old, sorted(new - old); print(len(new), "of", len(old), "locked packages kept")'
RUN rustup component add llvm-tools-preview \
    && cd /work/polyglot-source \
    && RUSTFLAGS='-C instrument-coverage -C codegen-units=1' CARGO_PROFILE_PYTHON_RELEASE_DEBUG=1 \
       CARGO_PROFILE_PYTHON_RELEASE_LTO=off CARGO_PROFILE_PYTHON_RELEASE_CODEGEN_UNITS=1 CARGO_PROFILE_PYTHON_RELEASE_STRIP=none \
       MATURIN_PEP517_ARGS='--locked' \
       /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/polyglot-source -w /work/wheels
RUN /opt/venv/bin/pip install --no-index --no-deps /work/wheels/polyglot_sql-*.whl \
    && cd /tmp && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import polyglot_sql; assert polyglot_sql.__version__ == "0.14.1", polyglot_sql.__version__; print(type(polyglot_sql.parse("SELECT 1", dialect="generic")[0]).__name__)'
RUN { python3 --version; rustc --version; /opt/venv/bin/pip show polyglot-sql maturin | grep -E '^(Name|Version):'; echo 'polyglot-sql 0.14.1 crate (crates/polyglot-sql in the sdist)'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-polyglot-sql-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/polyglot-source/crates/polyglot-sql/src /work/polyglot-source/crates/polyglot-sql/src
COPY --from=build /work/polyglot-source/crates/polyglot-sql-python/src /work/polyglot-source/crates/polyglot-sql-python/src
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov /usr/local/bin/llvm-cov
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata /usr/local/bin/llvm-profdata
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY harness.py replay.py fuzz.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
