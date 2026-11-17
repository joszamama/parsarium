# AFL++ instruments the parser family under simplesamlphp/xml-common's DOMDocumentFactory::fromString: pinned
# libxml2 2.15.4 XML parser sources (parser.c, parserInternals.c, SAX2.c) plus the PHP 8.5.12 ext/dom sources
# that load a Dom\XMLDocument from a string: xml_document.c (Dom\XMLDocument::createFromString, which
# fromString calls) and document.c (dom_document_parser, the shared libxml2 parse call). The build stage is
# the veewee/xml overlay's; namespace_compat.c and ext/libxml/libxml.c stay uninstrumented for the same
# traversal reasons. The package and its assert dependencies are interpreted PHP and reach AFL++ only
# through these sources.
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
RUN printf 'src:ext/dom/xml_document.c\nsrc:ext/dom/document.c\n' > /work/afl-allowlist-php.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt CC=afl-clang-fast CXX=afl-clang-fast++ CFLAGS='-O1 -g' PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig \
    ./configure --prefix=/opt/php --enable-cli --disable-all --with-libxml --enable-dom --without-pcre-jit \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt make -j8 && make install
RUN for object in $(find . -name '*.o' | sort); do \
        if nm "$object" | grep -q __afl_area_ptr; then echo "php-8.5.12/${object#./}"; fi; \
    done >> /work/afl-instrumented-objects.txt && cat /work/afl-instrumented-objects.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS package
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/simplesamlphp/xml-common/legacy.zip/c50b33dfc4384c772e921c6072bded9b67081c03 --output /work/simplesamlphp-xml-common.zip \
    && echo '99a309a70d7c481ce6b707c3e56299629dc50e61955f35c459f1f64c9b07bf6c  /work/simplesamlphp-xml-common.zip' | sha256sum --check \
    && rm -rf /work/x && unzip -q /work/simplesamlphp-xml-common.zip -d /work/x \
    && mkdir -p /work/vendor/simplesamlphp && mv /work/x/simplesamlphp-* /work/vendor/simplesamlphp/xml-common \
    && echo '20c17d8b8c48a600800dfd14f95d5cb9ff47066a9641ddeab48dc54aec96e331  /work/vendor/simplesamlphp/xml-common/LICENSE' | sha256sum --check \
    && echo '0bee113cebaa1efddb4f6b1fb5f07c1fd2d3df262534eed622bcc5d3015ecd66  /work/vendor/simplesamlphp/xml-common/composer.json' | sha256sum --check \
    && echo '66c9fc061682207136d843d29d09b8e6800ddf95546b123d314f6bf27ba233f8  /work/vendor/simplesamlphp/xml-common/src/XML/DOMDocumentFactory.php' | sha256sum --check \
    && echo '00f511e99a9360b284bed289ea1facd4b2f2744a4bfaa81da63bda60399595a5  /work/vendor/simplesamlphp/xml-common/src/XML/Assert/Assert.php' | sha256sum --check
RUN curl --fail --location --retry 3 https://codeload.github.com/simplesamlphp/assert/legacy.zip/33dcdeac629fa84a049f63738c30ecebdcb53061 --output /work/simplesamlphp-assert.zip \
    && echo '8caf9c764fa80a5e05a814bd83e220d87475575295c01a78d1c8a8edbe53ed16  /work/simplesamlphp-assert.zip' | sha256sum --check \
    && rm -rf /work/x && unzip -q /work/simplesamlphp-assert.zip -d /work/x \
    && mkdir -p /work/vendor/simplesamlphp && mv /work/x/simplesamlphp-* /work/vendor/simplesamlphp/assert \
    && echo '20c17d8b8c48a600800dfd14f95d5cb9ff47066a9641ddeab48dc54aec96e331  /work/vendor/simplesamlphp/assert/LICENSE' | sha256sum --check \
    && echo 'a71096adba1f3da589d2c0e2f3391bb0705bbac4d3ffd53a25582f53bde18c1b  /work/vendor/simplesamlphp/assert/composer.json' | sha256sum --check \
    && echo 'd859717ba0ed4f83faa30a0edc43831f57704b9db901e332902559d05e6c7a87  /work/vendor/simplesamlphp/assert/src/Assert.php' | sha256sum --check
RUN curl --fail --location --retry 3 https://codeload.github.com/webmozarts/assert/legacy.zip/ff31ad6efc62e66e518fbab1cde3453d389bcdc8 --output /work/webmozart-assert.zip \
    && echo '23059de8c31f3c16f9c8b3e10a4b5394464aae2b2a06bb223c90846029c92b4f  /work/webmozart-assert.zip' | sha256sum --check \
    && rm -rf /work/x && unzip -q /work/webmozart-assert.zip -d /work/x \
    && mkdir -p /work/vendor/webmozart && mv /work/x/webmozarts-* /work/vendor/webmozart/assert \
    && echo '5f82f5e664e8683e3d97d3bec6f74620b9d0a4d8669f9e617da96bce8767d4d3  /work/vendor/webmozart/assert/LICENSE' | sha256sum --check \
    && echo '93a39bdca52a5f0f56b7071f59060dde8e2f4f6f45a3073728e8d58f1435a899  /work/vendor/webmozart/assert/composer.json' | sha256sum --check \
    && echo '7cb6138a125b4a3c62d4dcac3a855e608f4545a911cb53ff9426c3ad20464c88  /work/vendor/webmozart/assert/src/Assert.php' | sha256sum --check

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
COPY --from=package /work/vendor /work/vendor
COPY projects/xml/php/simplesamlphp_xml_common/autoload.php projects/xml/php/simplesamlphp_xml_common/fuzz-target.php projects/xml/php/simplesamlphp_xml_common/harness.php projects/xml/php/simplesamlphp_xml_common/summary.php /work/
ENTRYPOINT ["/opt/php/bin/php", "/work/fuzz-target.php"]
