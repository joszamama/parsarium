# AFL++ instruments the parser family under symfony/dom-crawler: pinned libxml2 2.15.4 XML parser sources
# (parser.c, parserInternals.c, SAX2.c) plus PHP 8.5.12 ext/dom DOMDocument loading (document.c) and ext/libxml.
# The allowlist leaves libxml2 tree/XPath/dict code and the ext/dom navigation classes uninstrumented, so the
# AFL++ map holds parser-source tuples. Crawler itself is interpreted PHP and reaches AFL++ only through them.
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
WORKDIR /work/source/php-8.5.12
RUN printf 'src:ext/dom/document.c\nsrc:ext/libxml/libxml.c\n' > /work/afl-allowlist-php.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt CC=afl-clang-fast CXX=afl-clang-fast++ CFLAGS='-O1 -g' PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig \
    ./configure --prefix=/opt/php --enable-cli --disable-all --with-libxml --enable-dom --without-pcre-jit \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt make -j8 && make install
RUN for object in $(find . -name '*.o' | sort); do \
        if nm "$object" | grep -q __afl_area_ptr; then echo "php-8.5.12/${object#./}"; fi; \
    done >> /work/afl-instrumented-objects.txt && cat /work/afl-instrumented-objects.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS crawler
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/symfony/dom-crawler/legacy.zip/aa0674b52e1bd00502756fbaba8c982b446472e6 --output /work/dom-crawler.zip \
    && echo '7c538ae1812c8f479866e3b74431aa23c6ee75e3402334ceb875180e3a82e55b  /work/dom-crawler.zip' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/symfony/polyfill-ctype/legacy.zip/141046a8f9477948ff284fa65be2095baafb94f2 --output /work/polyfill-ctype.zip \
    && echo '922b0c6b24d1bcb6447d051edc1fc4526bcca5f88ddc4a27d885507872ceecc1  /work/polyfill-ctype.zip' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/symfony/polyfill-mbstring/legacy.zip/122889ed24dc000165bcbfd77ec412f15cbdfc6a --output /work/polyfill-mbstring.zip \
    && echo '560bc33ca56b79d9c285d9a2f14058ac489b6e6341df75c4e49cf87434c6e3ce  /work/polyfill-mbstring.zip' | sha256sum --check \
    && unzip -q /work/dom-crawler.zip -d /work/d && unzip -q /work/polyfill-ctype.zip -d /work/c && unzip -q /work/polyfill-mbstring.zip -d /work/m \
    && mkdir -p /work/vendor/symfony && mv /work/d/symfony-dom-crawler-* /work/vendor/symfony/dom-crawler \
    && mv /work/c/symfony-polyfill-ctype-* /work/vendor/symfony/polyfill-ctype && mv /work/m/symfony-polyfill-mbstring-* /work/vendor/symfony/polyfill-mbstring

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
COPY --from=crawler /work/vendor /work/vendor
COPY projects/xml/php/symfony_dom_crawler/autoload.php projects/xml/php/symfony_dom_crawler/fuzz-target.php projects/xml/php/symfony_dom_crawler/harness.php projects/xml/php/symfony_dom_crawler/summary.php /work/
ENTRYPOINT ["/opt/php/bin/php", "/work/fuzz-target.php"]
