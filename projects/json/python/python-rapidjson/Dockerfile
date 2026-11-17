FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl clang libclang-rt-14-dev libstdc++-12-dev llvm python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY build-requirements.lock /work/
# python-rapidjson 1.26 sdist; it vendors Tencent RapidJSON v1.1.0-763-g24b5e7a8 headers under rapidjson/include.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/55/6e/a1f7ac71cf915cd5cd51a274c2838b69f9d8ad8a2ed1ab7a20d8e7c4edc8/python_rapidjson-1.26.tar.gz -o /work/python-rapidjson.tar.gz \
    && echo 'db95af0b5ed5f89d4f91480477a0ea8c7646283e489dd9046e28503e85e08f98  /work/python-rapidjson.tar.gz' | sha256sum --check \
    && mkdir -p /work/rapidjson-source \
    && tar -xzf /work/python-rapidjson.tar.gz -C /work/rapidjson-source --strip-components=1 \
    && cd /work/rapidjson-source \
    && printf '%s\n' \
       '0f80b43dd26be1530cdfd81b3fb4374973f5873f7a676c90d1c9adac668a5b8b  rapidjson.cpp' \
       '43cd0f9afc832c7011518f4d779022e6c3609df7918e854006252b3b24b30f87  rapidjson/include/rapidjson/reader.h' \
       '4b1058fb40c0169fd4633fb821e75cb74450085d73935c49c77fbb25d1fb5be9  LICENSE' \
       'a140e5d46fe734a1c78f1a3c3ef207871dd75648be71fdda8e309b23ab8b1f32  rapidjson/license.txt' \
       | sha256sum --check \
    && test "$(cat rapidjson_exact_version.txt)" = 'v1.1.0-763-g24b5e7a8'
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
RUN cd /work/rapidjson-source \
    && CC=clang CXX=clang++ LDSHARED='clang -shared' LDCXXSHARED='clang++ -shared' \
       CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       CXXFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' \
       /opt/venv/bin/pip install --no-build-isolation --no-deps . \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import io, rapidjson; assert rapidjson.__version__ == "1.26", rapidjson.__version__; assert rapidjson.__rapidjson_exact_version__ == "v1.1.0-763-g24b5e7a8"; print(rapidjson.load(io.BytesIO(b"{\"ready\":true}")))'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; /opt/venv/bin/pip show python-rapidjson setuptools | grep -E '^(Name|Version):'; echo 'Tencent RapidJSON v1.1.0-763-g24b5e7a8 (vendored in the python-rapidjson 1.26 sdist)'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-python-rapidjson-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/rapidjson-source /work/rapidjson-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py structure.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
