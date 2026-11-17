FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl clang libclang-rt-21-dev llvm make python3 python3-venv xz-utils unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Same Expat source pin as projects/xml/python/xmltodict, untangle and defusedxml; CPython's pyexpat loads it through LD_LIBRARY_PATH.
RUN mkdir /work/wheels /work/expat \
    && curl --fail --location --retry 3 https://github.com/libexpat/libexpat/releases/download/R_2_10_0/expat-2.10.0.tar.xz --output /work/expat-2.10.0.tar.xz \
    && echo 'c624ba2998fc65df1163a49641ff3f9ab73138b11641d92c86bee0fb01b1bc7f  /work/expat-2.10.0.tar.xz' | sha256sum --check \
    && tar -xJf /work/expat-2.10.0.tar.xz --strip-components=1 -C /work/expat
# xmlschema 4.3.2 and its one runtime dependency elementpath 5.1.4 (installed py3-none-any wheels; each
# package directory and LICENSE must match its sdist byte for byte).
RUN curl --fail --location --retry 3 https://files.pythonhosted.org/packages/5c/fb/8be39dc47b0ed9bbc80f384906eed87fa974c9b377a7a430118c3b405550/xmlschema-4.3.2-py3-none-any.whl --output /work/wheels/xmlschema-4.3.2-py3-none-any.whl \
    && echo 'cf5c970a30f6ebcb3da35260e694704cc0b6794d8ace46125bb2a95e38ed9307  /work/wheels/xmlschema-4.3.2-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/55/f0/2431c2c8f77326757f2e2b1d79226c17b2abfe44a78a41c7d7b944e90732/xmlschema-4.3.2.tar.gz --output /work/xmlschema-sdist.tar.gz \
    && echo 'f3b33a21a2b2cdc404ddc3fb599d8bc1dee90b155d547370672e6e684746b8d6  /work/xmlschema-sdist.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/42/b0/b709cc33ccb0288f41f2d92dfd754d2ccf925cb9277a66effbc132cd004c/elementpath-5.1.4-py3-none-any.whl --output /work/wheels/elementpath-5.1.4-py3-none-any.whl \
    && echo '5ec8d7bb44b16c98414a6a95e20cb150f3cbfc3cac65edc14773288c7a937376  /work/wheels/elementpath-5.1.4-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/69/9d/766386c47959bb8b014242af8770c869350884a3c3f7054375576e11f30a/elementpath-5.1.4.tar.gz --output /work/elementpath-sdist.tar.gz \
    && echo '3c912a9c41311ac5244c038867670d7c0b0fec0e444813608e5b846dbb3428ac  /work/elementpath-sdist.tar.gz' | sha256sum --check \
    && mkdir /work/xmlschema-sdist /work/xmlschema-wheel /work/elementpath-sdist /work/elementpath-wheel \
    && tar -xzf /work/xmlschema-sdist.tar.gz --strip-components=1 -C /work/xmlschema-sdist \
    && unzip -q /work/wheels/xmlschema-4.3.2-py3-none-any.whl -d /work/xmlschema-wheel \
    && diff -r --exclude=xmlschema.egg-info /work/xmlschema-sdist/xmlschema /work/xmlschema-wheel/xmlschema \
    && cmp /work/xmlschema-sdist/LICENSE /work/xmlschema-wheel/xmlschema-4.3.2.dist-info/licenses/LICENSE \
    && echo 'de71695b2db6819ee4478ef39f5f202aab9f0c8750168c2986467ea8e5fa2997  /work/xmlschema-sdist/LICENSE' | sha256sum --check \
    && grep -Fx 'License-Expression: MIT' /work/xmlschema-wheel/xmlschema-4.3.2.dist-info/METADATA \
    && tar -xzf /work/elementpath-sdist.tar.gz --strip-components=1 -C /work/elementpath-sdist \
    && unzip -q /work/wheels/elementpath-5.1.4-py3-none-any.whl -d /work/elementpath-wheel \
    && diff -r /work/elementpath-sdist/elementpath /work/elementpath-wheel/elementpath \
    && cmp /work/elementpath-sdist/LICENSE /work/elementpath-wheel/elementpath-5.1.4.dist-info/licenses/LICENSE \
    && echo '01a603b5de335fa4db21d918bfb868981e894b768d9b4e6a201488ae2ef3b9ea  /work/elementpath-sdist/LICENSE' | sha256sum --check \
    && grep -Fx 'License-Expression: MIT' /work/elementpath-wheel/elementpath-5.1.4.dist-info/METADATA
RUN cd /work/expat \
    && CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
       ./configure --prefix=/opt/expat --disable-static --without-xmlwf --without-examples --without-tests \
    && make -j4 && make install
ENV LD_LIBRARY_PATH=/opt/expat/lib
COPY runtime-requirements.lock /work/
# XMLResource's default iterparse is xml.etree.ElementTree.iterparse: the pure-Python iterparse/XMLPullParser
# driver over the C _elementtree XMLParser and TreeBuilder, which call pyexpat directly.
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/xmlschema-wheel/xmlschema /opt/venv/lib/python3.14/site-packages/xmlschema \
    && diff -r --exclude=__pycache__ /work/elementpath-wheel/elementpath /opt/venv/lib/python3.14/site-packages/elementpath \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import _elementtree, pyexpat, xml.etree.ElementTree as et; from xmlschema import XMLResource; from xmlschema.resources.xml_loader import XMLResourceLoader; assert XMLResourceLoader.iterparse is et.iterparse and et.iterparse.__module__ == "xml.etree.ElementTree"; assert et.XMLParser is _elementtree.XMLParser and et.TreeBuilder is _elementtree.TreeBuilder; assert XMLResource.__mro__[1] is XMLResourceLoader; assert pyexpat.EXPAT_VERSION == "expat_2.10.0", pyexpat.EXPAT_VERSION' \
    && { python3 --version; /opt/venv/bin/pip show xmlschema elementpath | grep -E '^(Name|Version):'; LLVM_PROFILE_FILE=/dev/null python3 -c 'import pyexpat; print(pyexpat.EXPAT_VERSION)'; clang --version | head -n 1; llvm-cov --version | grep -i version | head -n 1; sha256sum /work/expat/lib/xmlparse.c /opt/venv/lib/python3.14/site-packages/xmlschema/resources/xml_resource.py /opt/venv/lib/python3.14/site-packages/xmlschema/resources/xml_loader.py /usr/lib/python3.14/xml/etree/ElementTree.py | sed 's#/opt/venv/lib/python3.14/site-packages/##'; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm libstdc++6 python3 && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/expat/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-xmlschema-%p.profraw
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
