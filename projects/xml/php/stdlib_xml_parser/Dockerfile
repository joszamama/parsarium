FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm make pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://download.gnome.org/sources/libxml2/2.15/libxml2-2.15.4.tar.xz --output /work/libxml2-2.15.4.tar.xz \
    && echo '98087fd181d9070724f3fbc65c7377db03038eb92bd882374daff44940138821  /work/libxml2-2.15.4.tar.xz' | sha256sum --check \
    && curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/libxml2-2.15.4.tar.xz -C /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source \
    && cd /work/source && sha256sum php-8.5.12/LICENSE libxml2-2.15.4/Copyright > /work/licenses.txt \
    && sha256sum php-8.5.12/ext/xml/xml.c php-8.5.12/ext/xml/compat.c php-8.5.12/ext/xml/expat_compat.h php-8.5.12/ext/xml/php_xml.h > /work/xml-sources.txt
ENV CC=clang CXX=clang++ CFLAGS='-O0 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate'
WORKDIR /work/source/libxml2-2.15.4
RUN ./configure --prefix=/opt/libxml2 --disable-static --without-python --without-zlib --without-lzma --without-iconv --without-icu --without-http --without-debug \
    && make -j8 && make install
# Without --with-expat, ext/xml builds compat.c, its expat-compatible layer over the libxml2 push parser.
WORKDIR /work/source/php-8.5.12
RUN PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig ./configure --prefix=/opt/php --enable-cli --disable-all --with-libxml --enable-xml --without-pcre-jit \
    || { tail -40 config.log; exit 1; } \
    && make -j8 && make install \
    && test -f ext/xml/compat.o
RUN { /opt/php/bin/php -v | head -1; /opt/php/bin/php -r 'echo "libxml ", LIBXML_DOTTED_VERSION, PHP_EOL;'; clang --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb llvm python3 \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/libxml2/lib
WORKDIR /work
COPY --from=build /opt/libxml2 /opt/libxml2
COPY --from=build /opt/php /opt/php
COPY --from=build /work/toolchain.txt /work/licenses.txt /work/xml-sources.txt /work/
COPY --from=build /work/source/php-8.5.12/ext/xml /work/source/php-8.5.12/ext/xml
COPY --from=build /work/source/php-8.5.12/ext/libxml /work/source/php-8.5.12/ext/libxml
COPY --from=build /work/source/libxml2-2.15.4 /work/source/libxml2-2.15.4
COPY fuzz-target.php harness.php summary.php run-control.py run-control.sh target.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
