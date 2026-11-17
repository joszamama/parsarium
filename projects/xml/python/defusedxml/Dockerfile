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
# defusedxml 0.7.1 (installed py2.py3-none-any wheel; defusedxml/ must match the sdist byte for byte).
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/07/6c/aa3f2f849e01cb6a001cd8554a88d4c77c5c1a31c95bdf1cf9301e6d9ef4/defusedxml-0.7.1-py2.py3-none-any.whl --output /work/wheels/defusedxml-0.7.1-py2.py3-none-any.whl \
    && echo 'a352e7e428770286cc899e2542b6cdaedb2b4953ff269a210103ec58f6198a61  /work/wheels/defusedxml-0.7.1-py2.py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/0f/d5/c66da9b79e5bdb124974bfe172b4daf3c984ebd9c2a06e2b8a4dc7331c72/defusedxml-0.7.1.tar.gz --output /work/defusedxml-sdist.tar.gz \
    && echo '1bb3032db185915b62d7c6209c5a8792be6a32ab2fedacc84e01b52c51aa3e69  /work/defusedxml-sdist.tar.gz' | sha256sum --check \
    && mkdir /work/defusedxml-sdist /work/defusedxml-wheel && tar -xzf /work/defusedxml-sdist.tar.gz --strip-components=1 -C /work/defusedxml-sdist \
    && unzip -q /work/wheels/defusedxml-0.7.1-py2.py3-none-any.whl -d /work/defusedxml-wheel \
    && diff -r /work/defusedxml-sdist/defusedxml /work/defusedxml-wheel/defusedxml \
    && cmp /work/defusedxml-sdist/LICENSE /work/defusedxml-wheel/defusedxml-0.7.1.dist-info/LICENSE \
    && echo 'b80ce9da8c42a1f91079627fbbe2bf27210ae108a0ffe5f077d5b08e076c24c8  /work/defusedxml-sdist/LICENSE' | sha256sum --check \
    && grep -Fx 'License: PSFL' /work/defusedxml-wheel/defusedxml-0.7.1.dist-info/METADATA
RUN cd /work/expat \
    && CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
       ./configure --prefix=/opt/expat --disable-static --without-xmlwf --without-examples --without-tests \
    && make -j4 && make install
ENV LD_LIBRARY_PATH=/opt/expat/lib
COPY runtime-requirements.lock /work/
# defusedxml.ElementTree re-imports CPython's pure-Python ElementTree with _elementtree blocked, so its
# DefusedXMLParser subclasses the Python XMLParser (pyexpat callbacks in ElementTree.py), not the C one.
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/defusedxml-wheel/defusedxml /opt/venv/lib/python3.14/site-packages/defusedxml \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import pyexpat, xml.etree.ElementTree as stdlib; import defusedxml.ElementTree as d; base = d.DefusedXMLParser.__mro__[1]; assert base is not stdlib.XMLParser and base.__module__ == "xml.etree.ElementTree" and hasattr(base, "_start"); assert d.parse.__module__ == "defusedxml.common"; assert pyexpat.EXPAT_VERSION == "expat_2.10.0", pyexpat.EXPAT_VERSION' \
    && { python3 --version; /opt/venv/bin/pip show defusedxml | grep -E '^(Name|Version):'; LLVM_PROFILE_FILE=/dev/null python3 -c 'import pyexpat; print(pyexpat.EXPAT_VERSION)'; clang --version | head -n 1; llvm-cov --version | grep -i version | head -n 1; sha256sum /work/expat/lib/xmlparse.c /opt/venv/lib/python3.14/site-packages/defusedxml/ElementTree.py /opt/venv/lib/python3.14/site-packages/defusedxml/common.py /usr/lib/python3.14/xml/etree/ElementTree.py | sed 's#/opt/venv/lib/python3.14/site-packages/##'; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/expat/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-defusedxml-%p.profraw
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
