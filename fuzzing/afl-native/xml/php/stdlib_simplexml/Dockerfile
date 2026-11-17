# AFL++ instruments the parse path behind simplexml_load_string: pinned libxml2 2.15.4 XML parser sources
# (parser.c, parserInternals.c, SAX2.c, which builds the tree) plus PHP 8.5.12 ext/simplexml/simplexml.c
# (simplexml_load_string and the SimpleXMLElement wrapper). The allowlist leaves libxml2 tree/XPath/dict code,
# ext/libxml/libxml.c and the Zend engine uninstrumented. simplexml.c also holds the SimpleXMLElement
# traversal methods; the fuzz target never calls them, and build.py records what the traversal harness adds.
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 ca-certificates clang curl llvm make pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://download.gnome.org/sources/libxml2/2.15/libxml2-2.15.4.tar.xz --output /work/libxml2-2.15.4.tar.xz \
    && echo '98087fd181d9070724f3fbc65c7377db03038eb92bd882374daff44940138821  /work/libxml2-2.15.4.tar.xz' | sha256sum --check \
    && curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/libxml2-2.15.4.tar.xz -C /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source \
    && cd /work/source && sha256sum php-8.5.12/LICENSE libxml2-2.15.4/Copyright > /work/licenses.txt \
    && sha256sum php-8.5.12/ext/simplexml/simplexml.c php-8.5.12/ext/simplexml/php_simplexml.h > /work/simplexml-sources.txt
# Out-of-tree build: sources compile as ../parser.c, so each allowlist entry names exactly one file
# (AFL++ matches entries as path suffixes; a bare parser.c entry would also cover HTMLparser.c).
WORKDIR /work/source/libxml2-2.15.4/build
RUN printf 'src:../parser.c\nsrc:../parserInternals.c\nsrc:../SAX2.c\n' > /work/afl-allowlist-libxml2.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-libxml2.txt CC=afl-clang-fast CFLAGS='-O1 -g' \
    ../configure --prefix=/opt/libxml2 --disable-static --without-python --without-zlib --without-lzma --without-iconv --without-icu --without-http --without-debug \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-libxml2.txt make -j8 && make install
RUN for object in $(find . -name '*.o' | sort); do \
        if nm "$object" | grep -q __afl_area_ptr; then echo "libxml2-2.15.4/build/${object#./}"; fi; \
    done > /work/afl-instrumented-objects.txt && cat /work/afl-instrumented-objects.txt
WORKDIR /work/source/php-8.5.12
RUN printf 'src:ext/simplexml/simplexml.c\n' > /work/afl-allowlist-php.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt CC=afl-clang-fast CXX=afl-clang-fast++ CFLAGS='-O1 -g' PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig \
    ./configure --prefix=/opt/php --enable-cli --disable-all --with-libxml --enable-simplexml --without-pcre-jit \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt make -j8 && make install
RUN for object in $(find . -name '*.o' | sort); do \
        if nm "$object" | grep -q __afl_area_ptr; then echo "php-8.5.12/${object#./}"; fi; \
    done >> /work/afl-instrumented-objects.txt && cat /work/afl-instrumented-objects.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/libxml2/lib
WORKDIR /work
COPY --from=build /opt/libxml2 /opt/libxml2
COPY --from=build /opt/php /opt/php
COPY --from=build /work/afl-allowlist-libxml2.txt /work/afl-allowlist-php.txt /work/afl-instrumented-objects.txt /work/licenses.txt /work/simplexml-sources.txt /work/
COPY projects/xml/php/stdlib_simplexml/fuzz-target.php projects/xml/php/stdlib_simplexml/harness.php projects/xml/php/stdlib_simplexml/summary.php /work/
ENTRYPOINT ["/opt/php/bin/php", "/work/fuzz-target.php"]
