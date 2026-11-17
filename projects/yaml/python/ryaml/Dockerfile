FROM --platform=linux/arm64 rust@sha256:b78cfbe4c0fd96b8a06b259092f1f412cb3ad3c5aed89d188bc40a1b8637f8f6 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV PATH=/opt/venv/bin:$PATH
COPY build-requirements.lock /work/
# ryaml 0.5.1 sdist: src/lib.rs is the PyO3 module (loads -> serde_yaml::from_str -> pythonize);
# Cargo.lock pins serde_yaml 0.9.34+deprecated and its unsafe-libyaml 0.2.11 parser.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/91/c7/f7357990e2ee4958258fe8b8a65a1bcd5d7526d76a04c3a2a5c1707ee05c/ryaml-0.5.1.tar.gz -o /work/ryaml.tar.gz \
    && echo 'b092d15521016f567aace04365d0aa36bea4270f34ebe264ef9e071cea0a8381  /work/ryaml.tar.gz' | sha256sum --check \
    && mkdir -p /work/ryaml-source \
    && tar -xzf /work/ryaml.tar.gz -C /work/ryaml-source --strip-components=1 \
    && cd /work/ryaml-source \
    && printf '%s\n' \
       '443669ea11b26f2932af3d8ffcee565ce0bf157b88a9e3d8d6f4c8843992394a  src/lib.rs' \
       '54130acf7e86694d00e68868e29514f40a1ba134aedeed8b02de72924f2af0ef  py-src/ryaml/__init__.py' \
       'f623e2b49fe811f936f248feb56431ed7a178c8be8687b3061ff9aeb7bc6e2de  Cargo.lock' \
       'e7633cdb717b262a29e3f70c0423602839c544ada84e76a13bfdef1980335f76  LICENSE' \
       | sha256sum --check \
    && grep -Fx 'checksum = "673aac59facbab8a9007c7f6108d11f63b603f7cabff99fabf650fea5c32b861"' Cargo.lock \
    && grep -Fx 'checksum = "6a8b1a1a2ebf674015cc02edccce75287f1a0130d394307b36743c2f5d504b47"' Cargo.lock
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# --locked makes cargo refuse any dependency resolution that differs from the sdist Cargo.lock
# (cargo also checks every crate against its Cargo.lock checksum).
RUN rustup component add llvm-tools-preview \
    && RUSTFLAGS='-C instrument-coverage -C codegen-units=1' CARGO_PROFILE_RELEASE_DEBUG=1 MATURIN_PEP517_ARGS='--locked' \
       /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/ryaml-source -w /work/wheels \
    && test -f /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/unsafe-libyaml-0.2.11/src/scanner.rs \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/ryaml-0.5.1-*.whl \
    && cd /tmp \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import ryaml; print(ryaml.loads("ready: true"))'
RUN { python3 --version; rustc --version; /opt/venv/bin/pip show ryaml maturin | grep -E '^(Name|Version):'; \
      grep -A1 -E '^name = "(pyo3|pythonize|serde_yaml|unsafe-libyaml|indexmap)"$' /work/ryaml-source/Cargo.lock | tr '\n' ' '; echo; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-ryaml-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/ryaml-source/src /work/ryaml-source/src
COPY --from=build /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/unsafe-libyaml-0.2.11 /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/unsafe-libyaml-0.2.11
COPY --from=build /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/serde_yaml-0.9.34+deprecated /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/serde_yaml-0.9.34+deprecated
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov /usr/local/bin/llvm-cov
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata /usr/local/bin/llvm-profdata
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh expected.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
