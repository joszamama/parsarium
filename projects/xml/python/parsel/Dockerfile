FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl clang libclang-rt-21-dev llvm make pkg-config python3 python3-dev python3-venv python3-setuptools libxslt1-dev xz-utils unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Same libxml2 and lxml source pins as projects/xml/python/lxml: Parsel's "xml" type is lxml's XML parser.
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
# parsel 1.12.1 (installed py3-none-any wheel; its parsel/ must match the sdist byte for byte) and its runtime dependencies.
# frostwork is a prebuilt abi3 extension imported by w3lib.html at import time; Parsel's XML parse path does not call it.
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/e9/44/2ff782553b581b3d55632eb4f9de1dc792ca99de7e47f69e22af28a9ef2d/parsel-1.12.1-py3-none-any.whl --output /work/wheels/parsel-1.12.1-py3-none-any.whl \
    && echo 'cf74e09857329bddc02c13ae239a9b46f410dc5bd1d05361c8c2643a1a5a7149  /work/wheels/parsel-1.12.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/08/ae/f24b3aac56ba91a29c9d3a31c07a9ad4e9eb500e5d212742bb6d348edaef/cssselect-1.6.0-py3-none-any.whl --output /work/wheels/cssselect-1.6.0-py3-none-any.whl \
    && echo '6df6eab9b264c0f2092a6e386b33610e1684a25e27925ecebe25e3d97cbf3525  /work/wheels/cssselect-1.6.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/14/2f/967ba146e6d58cf6a652da73885f52fc68001525b4197effc174321d70b4/jmespath-1.1.0-py3-none-any.whl --output /work/wheels/jmespath-1.1.0-py3-none-any.whl \
    && echo 'a5663118de4908c91729bea0acadca56526eb2698e83de10cd116ae0f4e97c64  /work/wheels/jmespath-1.1.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/aa/51/c3a48500fd4f211126b09d07850df33874455c432b7e8e5e0cfef8fcf7ba/w3lib-2.6.0-py3-none-any.whl --output /work/wheels/w3lib-2.6.0-py3-none-any.whl \
    && echo 'e62ce6b7f845b5e8588223d44e64990673a0fefd6815d6b3f2e6d39bf9ef308c  /work/wheels/w3lib-2.6.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/ff/66/400ec9f82e63bb597bfdb8e0a59ef00d99e34e4fb83a908edb0c5df167f4/frostwork-0.2.2-cp310-abi3-manylinux2014_aarch64.manylinux_2_17_aarch64.whl --output /work/wheels/frostwork-0.2.2-cp310-abi3-manylinux2014_aarch64.manylinux_2_17_aarch64.whl \
    && echo '98f0a24eaacffddac21abfa0ea060cc170f65cd4570f0c7fbea3eeb11230e643  /work/wheels/frostwork-0.2.2-cp310-abi3-manylinux2014_aarch64.manylinux_2_17_aarch64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl --output /work/wheels/typing_extensions-4.16.0-py3-none-any.whl \
    && echo '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  /work/wheels/typing_extensions-4.16.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/c4/04/b7eca3afc99d9dc1178ad22b5a37597d09c259d00693052480f2b2bbca83/parsel-1.12.1.tar.gz --output /work/parsel-sdist.tar.gz \
    && echo 'f526df846f3a91e13f5499156ea3e755114834cd126b62cd1d784ef558f3a713  /work/parsel-sdist.tar.gz' | sha256sum --check \
    && mkdir /work/parsel-sdist /work/parsel-wheel && tar -xzf /work/parsel-sdist.tar.gz --strip-components=1 -C /work/parsel-sdist \
    && unzip -q /work/wheels/parsel-1.12.1-py3-none-any.whl -d /work/parsel-wheel \
    && echo '7c9a5bce33c5cb32fd5b172f6a0bf2691e19ab11b06503eab2d826f5c6dee90d  /work/parsel-sdist/LICENSE' | sha256sum --check \
    && echo '7c9a5bce33c5cb32fd5b172f6a0bf2691e19ab11b06503eab2d826f5c6dee90d  /work/parsel-wheel/parsel-1.12.1.dist-info/licenses/LICENSE' | sha256sum --check \
    && diff -r /work/parsel-sdist/parsel /work/parsel-wheel/parsel
COPY runtime-requirements.lock /work/
RUN python3 -m venv --system-site-packages /opt/venv \
    && CC=clang CXX=clang++ WITHOUT_CYTHON=true STATIC_DEPS=false /opt/venv/bin/pip install --no-build-isolation --no-binary=lxml /work/lxml.tar.gz \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/parsel-wheel/parsel /opt/venv/lib/python3.14/site-packages/parsel \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import parsel, cssselect, jmespath, w3lib, frostwork; from importlib.metadata import version; from lxml import etree; from parsel.selector import SafeXMLParser, _ctgroup; assert version("parsel") == "1.12.1"; assert _ctgroup["xml"]["_parser"] is SafeXMLParser; assert etree.LIBXML_VERSION == (2, 15, 4) == etree.LIBXML_COMPILED_VERSION' \
    && ldd /opt/venv/lib/python3.14/site-packages/lxml/etree*.so | grep -F '/opt/libxml2/lib/libxml2.so.16' \
    && { python3 --version; /opt/venv/bin/pip show parsel lxml cssselect jmespath w3lib frostwork typing-extensions | grep -E '^(Name|Version):'; clang --version | head -1; llvm-cov --version | grep -i version | head -1; python3 -c 'import pyexpat; print("oracle", pyexpat.EXPAT_VERSION)'; sha256sum /work/libxml2/parser.c /opt/venv/lib/python3.14/site-packages/parsel/selector.py | sed 's#/opt/venv/lib/python3.14/site-packages/##'; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libxslt1.1 libstdc++6 && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/libxml2/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-parsel-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
# Fixed string hashing keeps Parsel's Python line paths repeatable for AFL++ feedback.
ENV PYTHONHASHSEED=0
WORKDIR /work
COPY --from=build /opt/libxml2 /opt/libxml2
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/libxml2 /work/libxml2
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py oracle.py fuzz.py replay.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
