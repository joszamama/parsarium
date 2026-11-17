# AFL++ instruments the parser family under saloonphp/xml-wrangler: pinned libxml2 2.15.4 XML parser and reader
# sources (parser.c, parserInternals.c, SAX2.c, xmlreader.c) plus PHP 8.5.12 ext/xmlreader (XMLReader, used by the
# veewee/xml Reader) and ext/dom DOMDocument loading (document.c, used by veewee/xml xml_decode). The allowlist
# leaves libxml2 tree/save/XPath/dict code, ext/libxml and the other ext/dom classes uninstrumented, so the AFL++
# map holds parser-source tuples. XML Wrangler and veewee/xml are interpreted PHP and reach AFL++ only through them.
# ext/sodium is built uninstrumented because php-standard-library's Composer bootstrap reads sodium constants.
FROM --platform=linux/arm64 parsarium/xml-php-saloon_xml_wrangler:local AS base

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 ca-certificates clang curl libsodium-dev llvm make pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://download.gnome.org/sources/libxml2/2.15/libxml2-2.15.4.tar.xz --output /work/libxml2-2.15.4.tar.xz \
    && echo '98087fd181d9070724f3fbc65c7377db03038eb92bd882374daff44940138821  /work/libxml2-2.15.4.tar.xz' | sha256sum --check \
    && curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/libxml2-2.15.4.tar.xz -C /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source
# Out-of-tree build: sources compile as ../parser.c, so each allowlist entry names exactly one file
# (AFL++ matches entries as path suffixes; a bare parser.c entry would also cover HTMLparser.c).
WORKDIR /work/source/libxml2-2.15.4/build
RUN printf 'src:../parser.c\nsrc:../parserInternals.c\nsrc:../SAX2.c\nsrc:../xmlreader.c\n' > /work/afl-allowlist-libxml2.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-libxml2.txt CC=afl-clang-fast CFLAGS='-O1 -g' \
    ../configure --prefix=/opt/libxml2 --disable-static --without-python --without-zlib --without-lzma --without-iconv --without-icu --without-http --without-debug \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-libxml2.txt make -j8 && make install
RUN for object in $(find . -name '*.o' | sort); do \
        if nm "$object" | grep -q __afl_area_ptr; then echo "libxml2-2.15.4/build/${object#./}"; fi; \
    done > /work/afl-instrumented-objects.txt && cat /work/afl-instrumented-objects.txt
WORKDIR /work/source/php-8.5.12
RUN printf 'src:ext/xmlreader/php_xmlreader.c\nsrc:ext/dom/document.c\n' > /work/afl-allowlist-php.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt CC=afl-clang-fast CXX=afl-clang-fast++ CFLAGS='-O1 -g' PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig \
    ./configure --prefix=/opt/php --enable-cli --disable-all --with-libxml --enable-dom --enable-xmlreader --with-sodium --without-pcre-jit \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt make -j8 && make install
RUN for object in $(find . -name '*.o' | sort); do \
        if nm "$object" | grep -q __afl_area_ptr; then echo "php-8.5.12/${object#./}"; fi; \
    done >> /work/afl-instrumented-objects.txt && cat /work/afl-instrumented-objects.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb libsodium23 \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/libxml2/lib
WORKDIR /work
COPY --from=build /opt/libxml2 /opt/libxml2
COPY --from=build /opt/php /opt/php
COPY --from=build /work/afl-allowlist-libxml2.txt /work/afl-allowlist-php.txt /work/afl-instrumented-objects.txt /work/
# The Composer tree comes from the verified base image, whose build diffed every package against its hashed archive.
COPY --from=base /work/vendor /work/vendor
COPY projects/xml/php/saloon_xml_wrangler/fuzz-target.php projects/xml/php/saloon_xml_wrangler/harness.php projects/xml/php/saloon_xml_wrangler/summary.php /work/
ENTRYPOINT ["/opt/php/bin/php", "/work/fuzz-target.php"]
