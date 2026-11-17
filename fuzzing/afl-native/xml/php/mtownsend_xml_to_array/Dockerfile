# AFL++ instruments the parser family under mtownsend/xml-to-array's XmlToArray::convert: pinned libxml2 2.15.4
# XML parser sources (parser.c, parserInternals.c, SAX2.c, which builds the tree) plus PHP 8.5.12
# ext/dom/document.c (DOMDocument::loadXML, which convert calls with default options). The allowlist leaves
# libxml2 tree/XPath/dict code, the ext/dom node classes and ext/libxml/libxml.c uninstrumented: libxml.c frees
# DOM wrapper objects at shutdown, so instrumenting it lets traversal add a tuple that parsing did not cause.
# XmlToArray itself is interpreted PHP and reaches AFL++ only through these sources.
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
RUN printf 'src:ext/dom/document.c\n' > /work/afl-allowlist-php.txt
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
RUN curl --fail --location --retry 3 https://codeload.github.com/mtownsend5512/xml-to-array/legacy.zip/8e4b08ae0f56f1e2a77b4b88a0e17bce0200350e --output /work/xml-to-array.zip \
    && echo '57a261f641eee98d20e27600e4846ebbcb05150277a67aa167f07ab3b3ce7e2c  /work/xml-to-array.zip' | sha256sum --check \
    && unzip -q /work/xml-to-array.zip -d /work/x \
    && mkdir -p /work/vendor/mtownsend && mv /work/x/mtownsend5512-xml-to-array-* /work/vendor/mtownsend/xml-to-array \
    && echo '435e9871353b2cd07083f10183e7c905c9dc0b291cd343327deaae1748302009  /work/vendor/mtownsend/xml-to-array/LICENSE.md' | sha256sum --check \
    && echo '907ea73dab5567632ccab156ba18d1360dfb00ec785c51e8e1225f9d5aee12d7  /work/vendor/mtownsend/xml-to-array/src/XmlToArray.php' | sha256sum --check

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
COPY projects/xml/php/mtownsend_xml_to_array/autoload.php projects/xml/php/mtownsend_xml_to_array/fuzz-target.php projects/xml/php/mtownsend_xml_to_array/harness.php projects/xml/php/mtownsend_xml_to_array/summary.php /work/
ENTRYPOINT ["/opt/php/bin/php", "/work/fuzz-target.php"]
