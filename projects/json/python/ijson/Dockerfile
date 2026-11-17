FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl clang libclang-rt-14-dev llvm python3 python3-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY build-requirements.lock /work/
# ijson 3.6.0 sdist plus the yajl fork commit pinned as its cextern/yajl submodule at tag v3.6.0.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/75/61/4066af787ed25bfca02c3edd2d7fd489b1b5ca27b54b400b187e5f2865e7/ijson-3.6.0.tar.gz -o /work/ijson.tar.gz \
    && echo 'ec8f9265524e724905ecf00bdd061c374baaa8d5045ef50425695fb06efb45f5  /work/ijson.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/rtobar/yajl/tar.gz/dd88e2ea2fc3f045722f6fee362af2643b5394f5 -o /work/yajl.tar.gz \
    && echo '071d41d073c1485a37e90e41aa8917e541861b9243911d4d8ac68394ee938f07  /work/yajl.tar.gz' | sha256sum --check \
    && mkdir -p /work/ijson-source/cextern/yajl \
    && tar -xzf /work/ijson.tar.gz -C /work/ijson-source --strip-components=1 \
    && tar -xzf /work/yajl.tar.gz -C /work/ijson-source/cextern/yajl --strip-components=1 \
    && cd /work/ijson-source \
    && printf '%s\n' \
       '9f077fdd8d82c108756e85e9b3bc501d3eced19fcbb63d95a5ac17680cb63444  src/ijson/backends/ext/_yajl2/items.c' \
       'dd6249f880f580dda27c37e473c0a90e1713a4d46b080b9c6414365764ca3877  src/ijson/backends/ext/_yajl2/basic_parse.c' \
       'e5c6f4cfe2d71620ea58a4aa9f9b1c61bf6b0e91fbd0e188e0998fe6c3cf8d00  LICENSE.txt' \
       '83f9c4dadbd4d6f57176e6182b0d9ec79f31eb6c864d90bd15bdd1a476c40435  cextern/yajl/src/yajl_parser.c' \
       '3432970d25a9cbd0f1cb8209831a1675648cb6a6168ad8a316050a6ef6db6dde  cextern/yajl/src/yajl_lex.c' \
       '054bf2c11686c5442850b1da58ad592e3d1d2a236a362e67279b957f8e662f5a  cextern/yajl/COPYING' \
       | sha256sum --check
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-deps --require-hashes -r /work/build-requirements.lock
# IJSON_EMBED_YAJL=1 is ijson's own build path for compiling yajl into _yajl2 (used for its macOS/Windows wheels).
RUN cd /work/ijson-source \
    && CC=clang LDSHARED='clang -shared' \
       CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' IJSON_EMBED_YAJL=1 IJSON_BUILD_YAJL2C=1 \
       /opt/venv/bin/pip install --no-build-isolation --no-deps . \
    && cd /work \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import io, ijson; assert ijson.__version__ == "3.6.0"; assert ijson.backend_name == "yajl2_c", ijson.backend_name; print(list(ijson.items(io.BytesIO(b"{\"ready\":true}"), "")))'
RUN { python3 --version; clang --version | head -1; llvm-cov --version | grep -i version | head -1; /opt/venv/bin/pip show ijson setuptools | grep -E '^(Name|Version):'; echo 'yajl rtobar/yajl@dd88e2ea2fc3f045722f6fee362af2643b5394f5 (2.1.1)'; } > /work/toolchain.txt

FROM --platform=linux/arm64 debian@sha256:ec8534cda2cb30f29f44f23e135297af7a1496f2990fd8e4e84aa36b081a757a
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/tmp/parsarium-ijson-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/ijson-source /work/ijson-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py replay.py fuzz.py run-control.py merge-native-coverage.py run-control.sh /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
