FROM --platform=linux/arm64 rust@sha256:b78cfbe4c0fd96b8a06b259092f1f412cb3ad3c5aed89d188bc40a1b8637f8f6 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl python3 python3-dev python3-venv clang libclang-rt-14-dev g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV PATH=/opt/venv/bin:$PATH
COPY build-requirements.lock runtime-requirements.lock ./
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/b4/fc/1203d011145c98ddce3cd2f505bb54375ef8d43223053df6bfcf3c746f46/pydantic-2.14.3.tar.gz -o /work/pydantic.tar.gz \
    && echo '1054f237f4d4733e5a30e1e2333bd33a2004ab9ab1510bd053a9a31bb48e232d  /work/pydantic.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/9c/0f/34f9ce4ba701dd0b815033ef94d99b56f66200e578ee6052aa3ac26f064e/pydantic_core-2.50.4.tar.gz -o /work/core.tar.gz \
    && echo 'aead3b74b68396bf0feab5d57e050b730ded7df55853c1e048a87e00aaf033c6  /work/core.tar.gz' | sha256sum --check \
    && mkdir /work/core-source && tar -xzf /work/core.tar.gz -C /work/core-source --strip-components=1 \
    && grep -A3 '^name = "jiter"' /work/core-source/Cargo.lock | grep -q 'version = "0.18.0"'
RUN rustup component add llvm-tools-preview \
    && RUSTFLAGS='-C instrument-coverage -C codegen-units=1' CARGO_PROFILE_RELEASE_DEBUG=1 \
       /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/core-source -w /work/wheels
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f8/58/5965955898e16bee17c8379eae12194993bf641c4629016991248b862069/atheris-3.0.0.tar.gz -o /work/atheris.tar.gz \
    && echo '1f0929c7bc3040f3fe4102e557718734190cf2d7718bbb8e3ce6d3eb56ef5bb3  /work/atheris.tar.gz' | sha256sum --check \
    && mkdir /work/atheris-source && tar -xzf /work/atheris.tar.gz -C /work/atheris-source --strip-components=1 \
    && printf '%s\n' 'wheel==0.48.0 --hash=sha256:3217dcc807155e45db462d7ef2431f5ddda0d7273b700d05a67b271ceb1287ab' 'packaging==26.3 --hash=sha256:d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c' 'pybind11==3.1.0 --hash=sha256:b8488090f8acffbcb6b5d6a85571a6827a0a2981ffb75e5a0b27b87c4a6b7dd0' | /opt/venv/bin/pip install --no-deps --require-hashes -r /dev/stdin \
    && LIBFUZZER_LIB=/usr/lib/llvm-14/lib/clang/14.0.6/lib/linux/libclang_rt.fuzzer-aarch64.a \
       /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/atheris-source -w /work/wheels
RUN /opt/venv/bin/pip install --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/pydantic_core-*.whl /work/wheels/atheris-*.whl \
    && /opt/venv/bin/python -c 'from pydantic import TypeAdapter; from typing import Any; print(TypeAdapter(Any).validate_json(b"{\"ready\":true}"))' \
    && find /usr/local/cargo/registry/cache -name jiter-0.18.0.crate -exec sha256sum {} + | grep '^49e31424b61d85292bd805dbf643c3ccc44f5f3871fb751209b889ee70585029 '
RUN { python3 --version; rustc --version; /opt/venv/bin/pip show pydantic pydantic-core atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-pydantic-%p.profraw
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov /usr/local/bin/llvm-cov
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata /usr/local/bin/llvm-profdata
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY --from=build /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/jiter-0.18.0 /usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/jiter-0.18.0
COPY harness.py replay.py fuzz.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
