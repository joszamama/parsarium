# AFL++ instruments the parser family under imangazaliev/didom: pinned libxml2 2.15.4 XML parser sources
# (parser.c, parserInternals.c, SAX2.c, which builds the tree) plus PHP 8.5.12 ext/dom/document.c
# (DOMDocument::loadXML, which imangazaliev/didom calls). The allowlist leaves libxml2 tree/XPath/dict code, the
# ext/dom node classes and ext/libxml/libxml.c uninstrumented: libxml.c frees DOM wrapper objects at
# shutdown, so instrumenting it lets traversal add a tuple that parsing did not cause.
# imangazaliev/didom itself is interpreted PHP and reaches AFL++ only through these sources.
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
RUN curl --fail --location --retry 3 https://codeload.github.com/Imangazaliev/DiDOM/legacy.zip/50fa6595d14f22c0c984efed5c818485cf548136 --output /work/didom.zip \
    && echo '35124c32ae958be5b73e46c2f8e4cf8fd65e5b64c0e83d7fe72de5eea48cf762  /work/didom.zip' | sha256sum --check \
    && unzip -q /work/didom.zip -d /work/x \
    && mkdir -p /work/vendor/imangazaliev && mv /work/x/Imangazaliev-* /work/vendor/imangazaliev/didom \
    && echo 'deff0cbe9b4905fd71e13219816aa435aa750835de76d0820cf96e9ec89aaef1  /work/vendor/imangazaliev/didom/LICENSE' | sha256sum --check \
    && echo '451f3517c35e767d2ff913e10151ece5f061384bd8def697768a24bcd566310e  /work/vendor/imangazaliev/didom/composer.json' | sha256sum --check \
    && echo 'fffadc6f50b187a210a36fbb29b629a7f4591d41c0719b565f65bb2cf24b8f91  /work/vendor/imangazaliev/didom/src/DiDom/Document.php' | sha256sum --check

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
COPY projects/xml/php/didom/autoload.php projects/xml/php/didom/fuzz-target.php projects/xml/php/didom/harness.php projects/xml/php/didom/summary.php /work/
ENTRYPOINT ["/opt/php/bin/php", "/work/fuzz-target.php"]
