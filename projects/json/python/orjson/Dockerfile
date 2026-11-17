FROM --platform=linux/arm64 rust@sha256:b78cfbe4c0fd96b8a06b259092f1f412cb3ad3c5aed89d188bc40a1b8637f8f6 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl python3 python3-dev python3-venv clang libclang-rt-14-dev g++ \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV PATH=/opt/venv/bin:$PATH
COPY build-requirements.lock ./
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f2/72/380b97dc45bd162d23afe5194721ef678d9eac7cfaa549fe2873f7f0a518/orjson-3.13.0.tar.gz -o /work/orjson.tar.gz \
    && echo 'd1de5eb04485110c5da4c657e49168995d55e076b1ce60f1a042e254f4186c4f  /work/orjson.tar.gz' | sha256sum --check \
    && mkdir /work/orjson-source && tar -xzf /work/orjson.tar.gz -C /work/orjson-source --strip-components=1
RUN rustup component add llvm-tools-preview \
    && RUSTFLAGS='-C instrument-coverage -C codegen-units=1' CARGO_PROFILE_RELEASE_DEBUG=1 CARGO_PROFILE_RELEASE_LTO=off \
       /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/orjson-source -w /work/wheels
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/f8/58/5965955898e16bee17c8379eae12194993bf641c4629016991248b862069/atheris-3.0.0.tar.gz -o /work/atheris.tar.gz \
    && echo '1f0929c7bc3040f3fe4102e557718734190cf2d7718bbb8e3ce6d3eb56ef5bb3  /work/atheris.tar.gz' | sha256sum --check \
    && mkdir /work/atheris-source && tar -xzf /work/atheris.tar.gz -C /work/atheris-source --strip-components=1 \
    && LIBFUZZER_LIB=/usr/lib/llvm-14/lib/clang/14.0.6/lib/linux/libclang_rt.fuzzer-aarch64.a \
       /opt/venv/bin/pip wheel --no-build-isolation --no-deps /work/atheris-source -w /work/wheels
RUN /opt/venv/bin/pip install --no-index --no-deps /work/wheels/orjson-*.whl /work/wheels/atheris-*.whl \
    && /opt/venv/bin/python -c 'import orjson; print(orjson.loads(b"{\"ready\":true}"))'
RUN { python3 --version; rustc --version; /opt/venv/bin/pip show orjson atheris | grep -E '^(Name|Version):'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-orjson-%p.profraw
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/orjson-source/src/deserialize /work/orjson-source/src/deserialize
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-cov /usr/local/bin/llvm-cov
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/rustlib/aarch64-unknown-linux-gnu/bin/llvm-profdata /usr/local/bin/llvm-profdata
COPY --from=build /usr/local/rustup/toolchains/1.99.1-aarch64-unknown-linux-gnu/lib/libLLVM.so.23.1-rust-1.99.1-stable /usr/local/lib/
COPY harness.py replay.py fuzz.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
