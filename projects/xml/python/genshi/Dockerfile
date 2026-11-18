FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl clang libclang-rt-21-dev llvm make python3 python3-venv xz-utils unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Same Expat source pin as projects/xml/python/xmltodict, untangle and jxmlease; CPython's pyexpat loads it through LD_LIBRARY_PATH.
RUN mkdir /work/wheels /work/expat \
    && curl --fail --location --retry 3 https://github.com/libexpat/libexpat/releases/download/R_2_10_0/expat-2.10.0.tar.xz --output /work/expat-2.10.0.tar.xz \
    && echo 'c624ba2998fc65df1163a49641ff3f9ab73138b11641d92c86bee0fb01b1bc7f  /work/expat-2.10.0.tar.xz' | sha256sum --check \
    && tar -xJf /work/expat-2.10.0.tar.xz --strip-components=1 -C /work/expat
# Genshi 0.7.12 (installed py3-none-any wheel, pure Python; genshi/ must match the sdist's Python files byte for byte,
# the sdist additionally ships the optional C speedups source _speedups.c, which the wheel does not build). No runtime dependencies on Python >= 3.9.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/03/49/af26aa9b8fbeec9d0aea2142320f1282009090b56bd6b4053629fd0c63e4/genshi-0.7.12-py3-none-any.whl --output /work/wheels/genshi-0.7.12-py3-none-any.whl \
    && echo '81a7852f935eaa317d4c55a15c12286e995c94f1ce9d1088bbce8690ac76c61b  /work/wheels/genshi-0.7.12-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/75/07/66dcb3df7b3995b692ada621ef3cb8cca98da74bd7a1f1758e8fa0fff706/genshi-0.7.12.tar.gz --output /work/genshi-sdist.tar.gz \
    && echo '4bca21a5a2515dabf985176be897a5b3b624626b4a9fcb648720b7c5fab71627  /work/genshi-sdist.tar.gz' | sha256sum --check \
    && mkdir /work/genshi-sdist /work/genshi-wheel && tar -xzf /work/genshi-sdist.tar.gz --strip-components=1 -C /work/genshi-sdist \
    && unzip -q /work/wheels/genshi-0.7.12-py3-none-any.whl -d /work/genshi-wheel \
    && diff -r --exclude=_speedups.c /work/genshi-sdist/genshi /work/genshi-wheel/genshi \
    && echo '1a1ea0fb71e2b729bd8a0f8284b6751ff0cca750d532a921e2273f4d11a56406  /work/genshi-sdist/COPYING' | sha256sum --check \
    && echo '1a1ea0fb71e2b729bd8a0f8284b6751ff0cca750d532a921e2273f4d11a56406  /work/genshi-wheel/genshi-0.7.12.dist-info/COPYING' | sha256sum --check \
    && grep -Fx 'License: BSD' /work/genshi-wheel/genshi-0.7.12.dist-info/METADATA
RUN cd /work/expat \
    && CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
       ./configure --prefix=/opt/expat --disable-static --without-xmlwf --without-examples --without-tests \
    && make -j4 && make install
ENV LD_LIBRARY_PATH=/opt/expat/lib
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/genshi-wheel/genshi /opt/venv/lib/python3.14/site-packages/genshi \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import pyexpat, genshi.input as gi; assert gi.expat.ParserCreate is pyexpat.ParserCreate; assert pyexpat.EXPAT_VERSION == "expat_2.10.0", pyexpat.EXPAT_VERSION' \
    && { python3 --version; /opt/venv/bin/pip show genshi | grep -E '^(Name|Version):'; LLVM_PROFILE_FILE=/dev/null python3 -c 'import pyexpat; print(pyexpat.EXPAT_VERSION)'; clang --version | head -n 1; llvm-cov --version | grep -i version | head -n 1; sha256sum /work/expat/lib/xmlparse.c /opt/venv/lib/python3.14/site-packages/genshi/input.py /opt/venv/lib/python3.14/site-packages/genshi/core.py | sed 's#/opt/venv/lib/python3.14/site-packages/##'; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/expat/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-genshi-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
# pyexpat passes CPython's hash secret to XML_SetHashSalt. PYTHONHASHSEED=0 zeroes it and Expat
# then draws a random salt per parser; a fixed nonzero seed keeps the Expat salt and hash paths repeatable.
ENV PYTHONHASHSEED=1
WORKDIR /work
COPY --from=build /opt/expat /opt/expat
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/expat/lib /work/expat/lib
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
