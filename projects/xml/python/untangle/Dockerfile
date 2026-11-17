FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl clang libclang-rt-21-dev llvm make python3 python3-venv xz-utils unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Same Expat source pin as projects/xml/python/xmltodict; CPython's pyexpat loads it through LD_LIBRARY_PATH.
RUN mkdir /work/wheels /work/expat \
    && curl --fail --location --retry 3 https://github.com/libexpat/libexpat/releases/download/R_2_10_0/expat-2.10.0.tar.xz --output /work/expat-2.10.0.tar.xz \
    && echo 'c624ba2998fc65df1163a49641ff3f9ab73138b11641d92c86bee0fb01b1bc7f  /work/expat-2.10.0.tar.xz' | sha256sum --check \
    && tar -xJf /work/expat-2.10.0.tar.xz --strip-components=1 -C /work/expat
# untangle 1.3.1 (installed py3-none-any wheel; untangle/__init__.py must match the sdist byte for byte) and its pinned defusedxml dependency.
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/be/32/efb0f536d2b22119f6a9ddaf29cac282e4ed432c15d349fb07d5018db863/untangle-1.3.1-py3-none-any.whl --output /work/wheels/untangle-1.3.1-py3-none-any.whl \
    && echo '987aed263b486e251db3999cc977542e2a030f344788c9d7f2bc70e89fae9438  /work/wheels/untangle-1.3.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/07/6c/aa3f2f849e01cb6a001cd8554a88d4c77c5c1a31c95bdf1cf9301e6d9ef4/defusedxml-0.7.1-py2.py3-none-any.whl --output /work/wheels/defusedxml-0.7.1-py2.py3-none-any.whl \
    && echo 'a352e7e428770286cc899e2542b6cdaedb2b4953ff269a210103ec58f6198a61  /work/wheels/defusedxml-0.7.1-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/3c/ba/6db19c34caa1fd66334fd1eb5f2f20df55c549b1968233fe898c4484bda5/untangle-1.3.1.tar.gz --output /work/untangle-sdist.tar.gz \
    && echo '6cac211f4d877935c1a62f543d40a596f3e4afe44380c4f6a2a1d4428214a5d0  /work/untangle-sdist.tar.gz' | sha256sum --check \
    && mkdir /work/untangle-sdist /work/untangle-wheel && tar -xzf /work/untangle-sdist.tar.gz --strip-components=1 -C /work/untangle-sdist \
    && unzip -q /work/wheels/untangle-1.3.1-py3-none-any.whl -d /work/untangle-wheel \
    && diff -r /work/untangle-sdist/src/untangle /work/untangle-wheel/untangle \
    && grep -Fx 'License-Expression: MIT' /work/untangle-wheel/untangle-1.3.1.dist-info/METADATA \
    && grep -Fx 'Requires-Dist: defusedxml==0.7.1' /work/untangle-wheel/untangle-1.3.1.dist-info/METADATA
RUN cd /work/expat \
    && CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
       ./configure --prefix=/opt/expat --disable-static --without-xmlwf --without-examples --without-tests \
    && make -j4 && make install
ENV LD_LIBRARY_PATH=/opt/expat/lib
COPY runtime-requirements.lock /work/
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/untangle-wheel/untangle /opt/venv/lib/python3.14/site-packages/untangle \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import pyexpat, untangle, xml.sax.expatreader; from defusedxml.sax import make_parser; from defusedxml.expatreader import DefusedExpatParser; p = make_parser(); assert type(p) is DefusedExpatParser and isinstance(p, xml.sax.expatreader.ExpatParser); assert pyexpat.EXPAT_VERSION == "expat_2.10.0", pyexpat.EXPAT_VERSION; assert untangle.parse.__module__ == "untangle"' \
    && { python3 --version; /opt/venv/bin/pip show untangle defusedxml | grep -E '^(Name|Version):'; LLVM_PROFILE_FILE=/dev/null python3 -c 'import pyexpat; print(pyexpat.EXPAT_VERSION)'; clang --version | head -n 1; llvm-cov --version | grep -i version | head -n 1; sha256sum /work/expat/lib/xmlparse.c /opt/venv/lib/python3.14/site-packages/untangle/__init__.py /usr/lib/python3.14/xml/sax/expatreader.py | sed 's#/opt/venv/lib/python3.14/site-packages/##'; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/expat/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-untangle-%p.profraw
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
