# AFL++ instruments the parser family under symfony/serializer's XmlEncoder::decode: pinned libxml2 2.15.4 XML
# parser sources (parser.c, parserInternals.c, SAX2.c, which builds the tree) plus PHP 8.5.12 ext/dom/document.c
# (DOMDocument::loadXML, which decode calls with LIBXML_NONET | LIBXML_NOBLANKS). The allowlist leaves libxml2
# tree/XPath/dict code, the ext/dom node and XPath classes and ext/libxml/libxml.c uninstrumented: libxml.c frees
# DOM wrapper objects at shutdown, so instrumenting it lets traversal add a tuple that parsing did not cause.
# XmlEncoder itself is interpreted PHP and reaches AFL++ only through these sources.
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
    && mkdir /work/source && tar -xJf /work/libxml2-2.15.4.tar.xz -C /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source
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
# ext/filter is enabled because XmlEncoder type-casts numeric attributes with filter_var().
WORKDIR /work/source/php-8.5.12
RUN printf 'src:ext/dom/document.c\n' > /work/afl-allowlist-php.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt CC=afl-clang-fast CXX=afl-clang-fast++ CFLAGS='-O1 -g' PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig \
    ./configure --prefix=/opt/php --enable-cli --disable-all --with-libxml --enable-dom --enable-filter --without-pcre-jit \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt make -j8 && make install
RUN for object in $(find . -name '*.o' | sort); do \
        if nm "$object" | grep -q __afl_area_ptr; then echo "php-8.5.12/${object#./}"; fi; \
    done >> /work/afl-instrumented-objects.txt && cat /work/afl-instrumented-objects.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS serializer
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/symfony/serializer/legacy.zip/05624c94507c3acf065b6486bb626f0d741af459 --output /work/serializer.zip \
    && echo '146260ba0f9fe210bc69a0a29535578b1c4ac07981b9dc15f1b8fe7bb79728de  /work/serializer.zip' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/symfony/deprecation-contracts/legacy.zip/feb1edf4e546af3b85c5caebe8359a20db230ca3 --output /work/deprecation-contracts.zip \
    && echo '284796ef0bf256f751e424a1f14763bc459cfe9fada8a0eb5eb3d2762587be0e  /work/deprecation-contracts.zip' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/symfony/polyfill-ctype/legacy.zip/141046a8f9477948ff284fa65be2095baafb94f2 --output /work/polyfill-ctype.zip \
    && echo '922b0c6b24d1bcb6447d051edc1fc4526bcca5f88ddc4a27d885507872ceecc1  /work/polyfill-ctype.zip' | sha256sum --check \
    && unzip -q /work/serializer.zip -d /work/s && unzip -q /work/deprecation-contracts.zip -d /work/d && unzip -q /work/polyfill-ctype.zip -d /work/c \
    && mkdir -p /work/vendor/symfony && mv /work/s/symfony-serializer-* /work/vendor/symfony/serializer \
    && mv /work/d/symfony-deprecation-contracts-* /work/vendor/symfony/deprecation-contracts && mv /work/c/symfony-polyfill-ctype-* /work/vendor/symfony/polyfill-ctype \
    && echo '18da7e490d2aa77197a0619b25bcc771a0110132a9d76071665718d3295e73cb  /work/vendor/symfony/serializer/LICENSE' | sha256sum --check

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
COPY --from=build /work/afl-allowlist-libxml2.txt /work/afl-allowlist-php.txt /work/afl-instrumented-objects.txt /work/
COPY --from=serializer /work/vendor /work/vendor
COPY projects/xml/php/symfony_serializer/autoload.php projects/xml/php/symfony_serializer/fuzz-target.php projects/xml/php/symfony_serializer/harness.php projects/xml/php/symfony_serializer/summary.php /work/
ENTRYPOINT ["/opt/php/bin/php", "/work/fuzz-target.php"]
