FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl clang libclang-rt-21-dev llvm make pkg-config python3 python3-dev python3-venv python3-setuptools libxslt1-dev xz-utils unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Same libxml2 and lxml source pins as projects/xml/python/lxml: Beautiful Soup's "xml" builder is lxml's XML parser.
RUN curl --fail --location --retry 3 https://download.gnome.org/sources/libxml2/2.15/libxml2-2.15.4.tar.xz --output /work/libxml2.tar.xz \
    && echo '98087fd181d9070724f3fbc65c7377db03038eb92bd882374daff44940138821  /work/libxml2.tar.xz' | sha256sum --check \
    && mkdir /work/libxml2 && tar -xJf /work/libxml2.tar.xz --strip-components=1 -C /work/libxml2 \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/23/ad/28ecd7cb894d172f3c9c80a075eeeb2017ac62e3632cee05a5f9493547eb/lxml-6.1.3.tar.gz --output /work/lxml.tar.gz \
    && echo '45222d94ddd511536f3b2f7d9deae3b2339b4ce0f075f1ca25703b07cad9dd21  /work/lxml.tar.gz' | sha256sum --check \
    && mkdir /work/lxml-src && tar -xzf /work/lxml.tar.gz --strip-components=1 -C /work/lxml-src \
    && echo '8fc2b568133516e46845d2147917adeee1648e70ae9ab5ed6c5417afef4ce855  /work/lxml-src/LICENSE.txt' | sha256sum --check
# beautifulsoup4 4.15.0 (installed py3-none-any wheel; its bs4/ must match the sdist byte for byte) and its two runtime dependencies.
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/88/c6/92fcd42f1ba33e1184263f25bfabf3d27c383410470f169e4b8163bf9c17/beautifulsoup4-4.15.0-py3-none-any.whl --output /work/wheels/beautifulsoup4-4.15.0-py3-none-any.whl \
    && echo 'd6f88de62e1d4e38ecb1077eb9724cd0eff29d2a08ca16a401e9b9e93f117cf9  /work/wheels/beautifulsoup4-4.15.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/cd/65/7fae69a095696195334a934eab23aeb12e2715e6c3f08025d2f91942750e/soupsieve-4.1.1-py3-none-any.whl --output /work/wheels/soupsieve-4.1.1-py3-none-any.whl \
    && echo '8ff3422dab0b720fb667ee79864d80531a0e57994a13eb701697719ffcb751f6  /work/wheels/soupsieve-4.1.1-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl --output /work/wheels/typing_extensions-4.16.0-py3-none-any.whl \
    && echo '481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8  /work/wheels/typing_extensions-4.16.0-py3-none-any.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/43/65/318323f98dbee45d42dff61d8f047181bc6f2268a9068cfad035a46be5af/beautifulsoup4-4.15.0.tar.gz --output /work/bs4-sdist.tar.gz \
    && echo '288e3ca7d54b06f2ac191970bc275c1939cb46d450b255bf6718b04aa37ab4f7  /work/bs4-sdist.tar.gz' | sha256sum --check \
    && mkdir /work/bs4-sdist /work/bs4-wheel && tar -xzf /work/bs4-sdist.tar.gz --strip-components=1 -C /work/bs4-sdist \
    && unzip -q /work/wheels/beautifulsoup4-4.15.0-py3-none-any.whl -d /work/bs4-wheel \
    && echo '55b4d8d4b1e5bc86d10efac91b74c87bcb77526b0f5b9edaf8b9cd2adc7397b2  /work/bs4-sdist/LICENSE' | sha256sum --check \
    && diff -r --exclude=tests /work/bs4-sdist/bs4 /work/bs4-wheel/bs4
RUN cd /work/libxml2 \
    && CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
       ./configure --prefix=/opt/libxml2 --enable-shared --disable-static --without-python --without-zlib --without-lzma --without-iconv --without-icu --without-http --without-modules --without-threads --without-catalog \
    && make -j4 && make install
ENV LD_LIBRARY_PATH=/opt/libxml2/lib
ENV PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig
ENV PATH=/opt/libxml2/bin:$PATH
COPY runtime-requirements.lock /work/
RUN python3 -m venv --system-site-packages /opt/venv \
    && CC=clang CXX=clang++ WITHOUT_CYTHON=true STATIC_DEPS=false /opt/venv/bin/pip install --no-build-isolation --no-binary=lxml /work/lxml.tar.gz \
    && /opt/venv/bin/pip install --no-index --find-links /work/wheels --no-deps --require-hashes -r /work/runtime-requirements.lock \
    && diff -r --exclude=__pycache__ /work/bs4-wheel/bs4 /opt/venv/lib/python3.14/site-packages/bs4 \
    && LLVM_PROFILE_FILE=/dev/null /opt/venv/bin/python -c 'import bs4, soupsieve, typing_extensions; from lxml import etree; from bs4.builder import builder_registry, LXMLTreeBuilderForXML; assert bs4.__version__ == "4.15.0"; assert builder_registry.lookup("xml") is LXMLTreeBuilderForXML; assert etree.LIBXML_VERSION == (2, 15, 4) == etree.LIBXML_COMPILED_VERSION' \
    && ldd /opt/venv/lib/python3.14/site-packages/lxml/etree*.so | grep -F '/opt/libxml2/lib/libxml2.so.16' \
    && { python3 --version; /opt/venv/bin/pip show beautifulsoup4 lxml soupsieve typing-extensions | grep -E '^(Name|Version):'; clang --version | head -1; llvm-cov --version | grep -i version | head -1; sha256sum /work/libxml2/parser.c /opt/venv/lib/python3.14/site-packages/bs4/builder/_lxml.py | sed 's#/opt/venv/lib/python3.14/site-packages/##'; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libxslt1.1 libstdc++6 && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/libxml2/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-bs4-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
# Fixed string hashing keeps Beautiful Soup's Python line paths repeatable for AFL++ feedback.
ENV PYTHONHASHSEED=0
WORKDIR /work
COPY --from=build /opt/libxml2 /opt/libxml2
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/libxml2 /work/libxml2
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py replay.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
