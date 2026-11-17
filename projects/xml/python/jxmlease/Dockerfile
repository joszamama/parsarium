FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl clang libclang-rt-21-dev llvm make python3 python3-venv xz-utils unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Same Expat source pin as projects/xml/python/xmltodict and untangle; CPython's pyexpat loads it through LD_LIBRARY_PATH.
RUN mkdir /work/wheels /work/expat \
    && curl --fail --location --retry 3 https://github.com/libexpat/libexpat/releases/download/R_2_10_0/expat-2.10.0.tar.xz --output /work/expat-2.10.0.tar.xz \
    && echo 'c624ba2998fc65df1163a49641ff3f9ab73138b11641d92c86bee0fb01b1bc7f  /work/expat-2.10.0.tar.xz' | sha256sum --check \
    && tar -xJf /work/expat-2.10.0.tar.xz --strip-components=1 -C /work/expat
# jxmlease 1.0.3 (installed py2.py3-none-any wheel; jxmlease/ must match the sdist byte for byte). It has no runtime dependencies.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/0d/d5/bea8c0334cb8439ea6b9549d84333e18160ff1044113c846d2b11602af85/jxmlease-1.0.3-py2.py3-none-any.whl --output /work/wheels/jxmlease-1.0.3-py2.py3-none-any.whl \
    && echo '6bbfaee0ecf7e287667c9b33fa70c2650265dcbf01518a2531a46b921c17cdaf  /work/wheels/jxmlease-1.0.3-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/8d/6a/b2944628e019c753894552c1499bf60e2cef9efea138756c5d66f0d5eb98/jxmlease-1.0.3.tar.gz --output /work/jxmlease-sdist.tar.gz \
    && echo '612c1575d8a87026dea096bb75acec7302dd69040fa23d9116e71e30d5e0839e  /work/jxmlease-sdist.tar.gz' | sha256sum --check \
    && mkdir /work/jxmlease-sdist /work/jxmlease-wheel && tar -xzf /work/jxmlease-sdist.tar.gz --strip-components=1 -C /work/jxmlease-sdist \
    && unzip -q /work/wheels/jxmlease-1.0.3-py2.py3-none-any.whl -d /work/jxmlease-wheel \
    && diff -r /work/jxmlease-sdist/jxmlease /work/jxmlease-wheel/jxmlease \
    && echo 'f45b614f8b1e759011de9310edc60c27bcc382a857bfae8fdf57c840e901e6ab  /work/jxmlease-sdist/LICENSE' | sha256sum --check \
    && echo 'f45b614f8b1e759011de9310edc60c27bcc382a857bfae8fdf57c840e901e6ab  /work/jxmlease-wheel/jxmlease-1.0.3.dist-info/LICENSE' | sha256sum --check \
    && grep -Fx 'License: MIT' /work/jxmlease-wheel/jxmlease-1.0.3.dist-info/METADATA
RUN cd /work/expat \
    && CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
       ./configure --prefix=/opt/expat --disable-static --without-xmlwf --without-examples --without-tests \
    && make -j4 && make install
ENV LD_LIBRARY_PATH=/opt/expat/lib
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/jxmlease-wheel/jxmlease /opt/venv/lib/python3.14/site-packages/jxmlease \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import pyexpat, jxmlease, jxmlease.xmlparser as xp; assert xp.expat.ParserCreate is pyexpat.ParserCreate; assert pyexpat.EXPAT_VERSION == "expat_2.10.0", pyexpat.EXPAT_VERSION; assert jxmlease.parse.__module__ == "jxmlease.xmlparser"' \
    && { python3 --version; /opt/venv/bin/pip show jxmlease | grep -E '^(Name|Version):'; LLVM_PROFILE_FILE=/dev/null python3 -c 'import pyexpat; print(pyexpat.EXPAT_VERSION)'; clang --version | head -n 1; llvm-cov --version | grep -i version | head -n 1; sha256sum /work/expat/lib/xmlparse.c /opt/venv/lib/python3.14/site-packages/jxmlease/_parsehandler.py /opt/venv/lib/python3.14/site-packages/jxmlease/xmlparser.py | sed 's#/opt/venv/lib/python3.14/site-packages/##'; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/expat/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-jxmlease-%p.profraw
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
