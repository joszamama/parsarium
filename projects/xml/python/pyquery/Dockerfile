FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl clang libclang-rt-21-dev llvm make pkg-config python3 python3-dev python3-venv python3-setuptools libxslt1-dev xz-utils unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Same libxml2 and lxml source pins as projects/xml/python/lxml and parsel: PyQuery(..., parser="xml") is lxml's XML parser.
RUN curl --fail --location --retry 3 https://download.gnome.org/sources/libxml2/2.15/libxml2-2.15.4.tar.xz --output /work/libxml2.tar.xz \
    && echo '98087fd181d9070724f3fbc65c7377db03038eb92bd882374daff44940138821  /work/libxml2.tar.xz' | sha256sum --check \
    && mkdir /work/libxml2 && tar -xJf /work/libxml2.tar.xz --strip-components=1 -C /work/libxml2 \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/23/ad/28ecd7cb894d172f3c9c80a075eeeb2017ac62e3632cee05a5f9493547eb/lxml-6.1.3.tar.gz --output /work/lxml.tar.gz \
    && echo '45222d94ddd511536f3b2f7d9deae3b2339b4ce0f075f1ca25703b07cad9dd21  /work/lxml.tar.gz' | sha256sum --check \
    && mkdir /work/lxml-src && tar -xzf /work/lxml.tar.gz --strip-components=1 -C /work/lxml-src \
    && echo '8fc2b568133516e46845d2147917adeee1648e70ae9ab5ed6c5417afef4ce855  /work/lxml-src/LICENSE.txt' | sha256sum --check
RUN cd /work/libxml2 \
    && CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
       ./configure --prefix=/opt/libxml2 --enable-shared --disable-static --without-python --without-zlib --without-lzma --without-iconv --without-icu --without-http --without-modules --without-threads --without-catalog \
    && make -j4 && make install
ENV LD_LIBRARY_PATH=/opt/libxml2/lib
ENV PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig
ENV PATH=/opt/libxml2/bin:$PATH
# pyquery 2.1.0 (installed py3-none-any wheel; its pyquery/ must match the sdist byte for byte) and cssselect 1.6.0.
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/2f/d2/5eab7f15bdb63c5281f625a003e999ef3f843c35972c936b07ea868cb854/pyquery-2.1.0-py3-none-any.whl --output /work/wheels/pyquery-2.1.0-py3-none-any.whl \
    && echo '74c9e65ea0cfbcf644a8c3fd438a3dedbcbbd497b9cb366a4f360dba72f8aebb  /work/wheels/pyquery-2.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/08/ae/f24b3aac56ba91a29c9d3a31c07a9ad4e9eb500e5d212742bb6d348edaef/cssselect-1.6.0-py3-none-any.whl --output /work/wheels/cssselect-1.6.0-py3-none-any.whl \
    && echo '6df6eab9b264c0f2092a6e386b33610e1684a25e27925ecebe25e3d97cbf3525  /work/wheels/cssselect-1.6.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c5/d8/955aef5c4ba7e01c67779a9856c4030aa89b6600b78544eae8a22a91185b/pyquery-2.1.0.tar.gz --output /work/pyquery-sdist.tar.gz \
    && echo '75238388750fc6e254b7a52f771027b9beb3a6202b88048bef52a00b0abeadbb  /work/pyquery-sdist.tar.gz' | sha256sum --check \
    && mkdir /work/pyquery-sdist /work/pyquery-wheel && tar -xzf /work/pyquery-sdist.tar.gz --strip-components=1 -C /work/pyquery-sdist \
    && unzip -q /work/wheels/pyquery-2.1.0-py3-none-any.whl -d /work/pyquery-wheel \
    && echo '6e96459ce221aca0d34a41d909f55d2bc8898b14e5e24e74cdd2a51ceb603cb6  /work/pyquery-sdist/LICENSE.txt' | sha256sum --check \
    && echo '6e96459ce221aca0d34a41d909f55d2bc8898b14e5e24e74cdd2a51ceb603cb6  /work/pyquery-wheel/pyquery-2.1.0.dist-info/licenses/LICENSE.txt' | sha256sum --check \
    && diff -r /work/pyquery-sdist/pyquery /work/pyquery-wheel/pyquery
COPY runtime-requirements.lock /work/
RUN python3 -m venv --system-site-packages /opt/venv \
    && CC=clang CXX=clang++ WITHOUT_CYTHON=true STATIC_DEPS=false /opt/venv/bin/pip install --no-build-isolation --no-binary=lxml /work/lxml.tar.gz \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/pyquery-wheel/pyquery /opt/venv/lib/python3.14/site-packages/pyquery \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import pyquery, cssselect; from importlib.metadata import version; from lxml import etree; assert version("pyquery") == "2.1.0"; assert etree.LIBXML_VERSION == (2, 15, 4) == etree.LIBXML_COMPILED_VERSION; assert type(pyquery.PyQuery(b"<r/>", parser="xml")[0]) is etree._Element' \
    && ldd /opt/venv/lib/python3.14/site-packages/lxml/etree*.so | grep -F '/opt/libxml2/lib/libxml2.so.16' \
    && { python3 --version; /opt/venv/bin/pip show pyquery lxml cssselect | grep -E '^(Name|Version):'; clang --version | head -1; llvm-cov --version | grep -i version | head -1; python3 -c 'import pyexpat; print("oracle", pyexpat.EXPAT_VERSION)'; sha256sum /work/libxml2/parser.c /opt/venv/lib/python3.14/site-packages/pyquery/pyquery.py | sed 's#/opt/venv/lib/python3.14/site-packages/##'; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libxslt1.1 libstdc++6 && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/libxml2/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-pyquery-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
# Fixed string hashing keeps pyquery's Python line paths repeatable for AFL++ feedback.
ENV PYTHONHASHSEED=0
WORKDIR /work
COPY --from=build /opt/libxml2 /opt/libxml2
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/libxml2 /work/libxml2
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py oracle.py fuzz.py replay.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
