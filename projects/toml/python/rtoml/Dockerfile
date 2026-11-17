FROM --platform=linux/arm64 rust@sha256:b78cfbe4c0fd96b8a06b259092f1f412cb3ad3c5aed89d188bc40a1b8637f8f6 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV PATH=/opt/venv/bin:$PATH
COPY build-requirements.lock /work/
# rtoml 0.14.0 sdist: src/*.rs is the PyO3 _rtoml module; its Cargo.lock pins toml 1.1.8,
# toml_parser 1.1.5 and toml_datetime 1.1.2 from crates.io.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/da/fb/ef915d0c607fb92674b16e15792ed9d254c9db0b3fbbea90b7be46fe3e2b/rtoml-0.14.0.tar.gz -o /work/rtoml.tar.gz \
    && echo 'e0f95a59e3fac6394985d59ce18a0c06f2176f2eb9dec2fb8c1105febaf05c59  /work/rtoml.tar.gz' | sha256sum --check \
    && mkdir -p /work/rtoml-source \
    && tar -xzf /work/rtoml.tar.gz -C /work/rtoml-source --strip-components=1 \
    && cd /work/rtoml-source \
    && printf '%s\n' \
       '8bf625d2f14f2eefb305ef255051ee8cd8de07be9fd11a955af57d7a572a8962  Cargo.lock' \
       '707bdb34c5b967650d5f87a0a6da6da5b8b323147fdc4f3abfd329ab2903a0b9  LICENSE' \
       '7e9b0601a310befb20ca3d149138cbfacdb39a5e1513d05d415243221a9d68e8  src/lib.rs' \
       '52f28a467f533d08c54b1fbea6fead2bfc132a84655f38f6ba995001a1252bae  src/de.rs' \
       'ad3e8d9f5852e79dfb9372790f78d92a052224de64803a8f50b51abcefa6bd26  src/datetime.rs' \
       'c344f04efba074ded87226b47696f7108db26d1382a69d40fe582cc5c760503a  python/rtoml/__init__.py' \
       | sha256sum --check \
    && grep -Fx 'License: MIT' PKG-INFO
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# --locked makes cargo refuse any dependency resolution that differs from the sdist Cargo.lock;
# cargo checks every downloaded crate against the Cargo.lock checksums.
RUN rustup component add llvm-tools-preview \
    && RUSTFLAGS='-C instrument-coverage -C codegen-units=1' CARGO_PROFILE_RELEASE_DEBUG=1 MATURIN_PEP517_ARGS='--locked' \
       /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/rtoml-source -w /work/wheels \
    && find /usr/local/cargo/registry/cache -name 'toml_parser-1.1.5+spec-1.1.0.crate' -exec sha256sum {} + | grep -q '^baa693a8032d7e1cada7d0041e96126df243179ff061456783ac7f12bda4744c ' \
    && find /usr/local/cargo/registry/cache -name 'toml-1.1.8+spec-1.1.0.crate' -exec sha256sum {} + | grep -q '^20489e00e4d8741d6be680764cc12e270655e375a20d1011e844a9c3379e678d ' \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/rtoml-0.14.0-*.whl \
    && diff -r --exclude=__pycache__ --exclude='_rtoml*.so' /work/rtoml-source/python/rtoml /opt/venv/lib/python3.11/site-packages/rtoml \
    && cd /tmp \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import rtoml; assert rtoml.__version__ == "0.14.0", rtoml.__version__; print(rtoml.loads("ready = true\n"))'
RUN { python3 --version; rustc --version; /opt/venv/bin/pip show rtoml maturin | grep -E '^(Name|Version):'; \
      for crate in toml toml_parser toml_datetime pyo3; do grep -A1 "^name = \"$crate\"$" /work/rtoml-source/Cargo.lock | tr '\n' ' '; echo; done; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-rtoml-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/rtoml-source/src /work/rtoml-source/src
COPY --from=build ["/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/toml_parser-1.1.5+spec-1.1.0", "/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/toml_parser-1.1.5+spec-1.1.0"]
COPY --from=build ["/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/toml-1.1.8+spec-1.1.0", "/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/toml-1.1.8+spec-1.1.0"]
COPY --from=build ["/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/toml_datetime-1.1.2+spec-1.1.0", "/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/toml_datetime-1.1.2+spec-1.1.0"]
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov /usr/local/bin/llvm-cov
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata /usr/local/bin/llvm-profdata
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY expected /work/expected
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
