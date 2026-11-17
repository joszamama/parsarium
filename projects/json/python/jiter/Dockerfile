FROM --platform=linux/arm64 rust@sha256:b78cfbe4c0fd96b8a06b259092f1f412cb3ad3c5aed89d188bc40a1b8637f8f6 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV PATH=/opt/venv/bin:$PATH
COPY build-requirements.lock /work/
# jiter 0.19.0 sdist; crates/jiter/src is the Jiter Rust parser, crates/jiter-python the PyO3 module.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/67/de/8dfd06a2153d8ab6a83a8ca8f8ae3ff860ce2fe324ee6a5d05294b621c2a/jiter-0.19.0.tar.gz -o /work/jiter.tar.gz \
    && echo 'ba3064f8be276d7cfb83c2fb85c858be533da2c2f80f9b048c3781b45a57a195  /work/jiter.tar.gz' | sha256sum --check \
    && mkdir -p /work/jiter-source \
    && tar -xzf /work/jiter.tar.gz -C /work/jiter-source --strip-components=1 \
    && cd /work/jiter-source \
    && printf '%s\n' \
       'c34ffc5279948596c1f40473becf1872e72df45287cbf19dfbfb630dd2bc983b  crates/jiter/src/parse.rs' \
       '12500816758ae151ea4e3b7266125fedfe821a546c39471b120dd4e465adb2f4  crates/jiter/src/python.rs' \
       '36fb8b259dcc0f9fb64f7bb8d663da9e4d60ee2984af53ffa2ed9001800af758  crates/jiter/src/string_decoder.rs' \
       'b0aadf83d15f600a5f62ca6be506f0172abf202f1f2f29cf7e3fe6e013b872db  crates/jiter/src/number_decoder.rs' \
       '3aef3ea6e3c23ea2095d4f4010e82b35be2b1b478b2029a2a3680b8f7294074f  crates/jiter-python/src/lib.rs' \
       '759a9868d0e438e88320e1332f12cbb78270665e757956952754a46f2de003b5  Cargo.lock' \
       '7c7134b9f7b978c03fca875517cf398db91f19bbb8109b6685e742aa3f57468e  LICENSE' \
       | sha256sum --check
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# --locked makes cargo refuse any dependency resolution that differs from the sdist Cargo.lock.
RUN rustup component add llvm-tools-preview \
    && RUSTFLAGS='-C instrument-coverage -C codegen-units=1' CARGO_PROFILE_RELEASE_DEBUG=1 MATURIN_PEP517_ARGS='--locked' \
       /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/jiter-source -w /work/wheels \
    && find /usr/local/cargo/registry/cache -name lexical-parse-float-1.0.6.crate -exec sha256sum {} + | grep -q '^52a9f232fbd6f550bc0137dcb5f99ab674071ac2d690ac69704593cb4abbea56 ' \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/jiter-0.19.0-*.whl \
    && cd /tmp \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import jiter; assert jiter.__version__ == "0.19.0", jiter.__version__; print(jiter.from_json(b"{\"ready\":true}"))'
RUN { python3 --version; rustc --version; /opt/venv/bin/pip show jiter maturin | grep -E '^(Name|Version):'; grep -A1 '^name = "pyo3"$' /work/jiter-source/Cargo.lock | tr '\n' ' '; echo; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-jiter-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/jiter-source/crates /work/jiter-source/crates
COPY --from=build /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/lexical-parse-float-1.0.6 /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/lexical-parse-float-1.0.6
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov /usr/local/bin/llvm-cov
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata /usr/local/bin/llvm-profdata
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
