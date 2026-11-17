FROM --platform=linux/arm64 rust@sha256:b78cfbe4c0fd96b8a06b259092f1f412cb3ad3c5aed89d188bc40a1b8637f8f6 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV PATH=/opt/venv/bin:$PATH
COPY build-requirements.lock /work/
# yaml-rs 0.1.6 sdist: src/ is the PyO3 module and its own loader (src/load/); Cargo.lock pins
# granit-parser, the lava-sh saphyr fork, pyo3 and lexical-core to git revisions.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/9f/2a/f4bcd7aa533a49cb3fd8acb66da41926465ed3ee763db017c902be46f612/yaml_rs-0.1.6.tar.gz -o /work/yaml_rs.tar.gz \
    && echo 'e57f7f8c0f78019e43833054cb8cf6354dff4e843d22ba87aa4c4d440ce617bd  /work/yaml_rs.tar.gz' | sha256sum --check \
    && mkdir -p /work/yaml-rs-source \
    && tar -xzf /work/yaml_rs.tar.gz -C /work/yaml-rs-source --strip-components=1 \
    && cd /work/yaml-rs-source \
    && printf '%s\n' \
       '1e06b517b3b57de5c96a6595f5bcae0cb3cce1cea2fa2793d6505b35f4d02ffe  src/lib.rs' \
       'e16615497200736ece61e2098c0fc2565ec3555550612526be597b2bf9ee8d18  src/load/loads.rs' \
       '9b28ddd8395a374861dd21ddfcd7625e558c19c82c1c6aca1ed2b61811e2014b  src/load/scalar.rs' \
       'b87b14c4071dd5f0ec18934277adf618104d2450a70eb0e7619bdf26c8f6b149  py-src/yaml_rs/_lib.py' \
       '7683e9bbea67ac66e9bb1d82290f6a067dc358afb9cd97dddddab1bc0369d0e1  Cargo.lock' \
       'ca2abdf695884c77ea4b4a5b64ca7b732d9d9dbade4eebc1c2e76c53e9e3bc83  UNLICENSE' \
       | sha256sum --check \
    && grep -F 'granit-parser?rev=e10ee63e049c2fff7390d5640c690e95c8d216a1#e10ee63e049c2fff7390d5640c690e95c8d216a1' Cargo.lock
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# The sdist's rust-toolchain.toml asks for an unpinned "nightly" (pyo3's nightly feature);
# RUSTUP_TOOLCHAIN pins the nightly of the 0.1.6 release date. --locked makes cargo refuse any
# resolution that differs from the sdist Cargo.lock (git dependencies at their locked revisions).
ENV RUSTUP_TOOLCHAIN=nightly-2026-07-07
RUN rustup toolchain install nightly-2026-07-07 --profile minimal --component llvm-tools-preview \
    && RUSTFLAGS='-C instrument-coverage -C codegen-units=1' CARGO_PROFILE_RELEASE_DEBUG=1 CARGO_PROFILE_RELEASE_LTO=false \
       CARGO_PROFILE_RELEASE_STRIP=false MATURIN_PEP517_ARGS='--locked' \
       /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/yaml-rs-source -w /work/wheels \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/yaml_rs-0.1.6-*.whl \
    && granit=$(find /usr/local/cargo/git/checkouts -maxdepth 2 -type d -path '*granit-parser-*/e10ee63' -print -quit) \
    && test "$granit" = /usr/local/cargo/git/checkouts/granit-parser-adcc536166983974/e10ee63 && ln -s "$granit" /work/granit-parser \
    && test -f /work/granit-parser/src/scanner.rs \
    && mkdir -p /work/llvm/bin /work/llvm/lib \
    && toolchain=$(rustc --print sysroot) \
    && cp "$toolchain"/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov "$toolchain"/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata /work/llvm/bin/ \
    && cp "$toolchain"/lib/libLLVM*.so* /work/llvm/lib/ \
    && cd /tmp \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import yaml_rs; assert yaml_rs.__version__ == "0.1.6"; print(yaml_rs.loads("ready: true"))'
RUN { python3 --version; rustc --version; /opt/venv/bin/pip show yaml-rs maturin | grep -E '^(Name|Version):'; \
      grep -A2 -E '^name = "(pyo3|granit-parser|saphyr|saphyr-parser|lexical-core)"$' /work/yaml-rs-source/Cargo.lock | tr '\n' ' '; echo; \
      readlink -f /work/granit-parser; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-yaml-rs-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/yaml-rs-source/src /work/yaml-rs-source/src
COPY --from=build /usr/local/cargo/git/checkouts/granit-parser-adcc536166983974/e10ee63 /usr/local/cargo/git/checkouts/granit-parser-adcc536166983974/e10ee63
COPY --from=build /work/llvm/bin/ /usr/local/bin/
COPY --from=build /work/llvm/lib/ /usr/local/lib/
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh expected.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
