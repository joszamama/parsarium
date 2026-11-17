FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates curl clang libclang-rt-21-dev llvm make pkg-config python3 python3-dev python3-venv python3-setuptools libxslt1-dev xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
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
RUN python3 -m venv --system-site-packages /opt/venv \
    && CC=clang CXX=clang++ WITHOUT_CYTHON=true STATIC_DEPS=false /opt/venv/bin/pip install --no-build-isolation --no-binary=lxml /work/lxml.tar.gz \
    && /opt/venv/bin/python -c 'from lxml import etree; print("lxml", etree.LXML_VERSION, "libxml2", etree.LIBXML_VERSION, "compiled", etree.LIBXML_COMPILED_VERSION)' \
    && { python3 --version; /opt/venv/bin/pip show lxml | grep -E '^(Name|Version):'; clang --version | head -1; llvm-cov --version | head -1; sha256sum /work/libxml2/parser.c; } > /work/toolchain.txt
RUN /opt/venv/bin/python -c 'from lxml import etree; assert etree.LIBXML_VERSION == (2, 15, 4); assert etree.LIBXML_COMPILED_VERSION == (2, 15, 4)' \
    && ldd /opt/venv/lib/python3.14/site-packages/lxml/etree*.so | grep -F '/opt/libxml2/lib/libxml2.so.16'

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libxslt1.1 libstdc++6 && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/libxml2/lib
ENV LLVM_PROFILE_FILE=/tmp/parsarium-lxml-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/libxml2 /opt/libxml2
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/libxml2 /work/libxml2
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
