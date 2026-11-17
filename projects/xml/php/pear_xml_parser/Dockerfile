# pear/xml_parser (XML_Parser 1.3.8) is interpreted PHP over ext/xml's xml_parser_create/xml_parse, which run the
# libxml2 push parser through ext/xml/compat.c. The image therefore pairs two coverage sources on one run:
# Xdebug line coverage for the package PHP source and Clang/LLVM source coverage for PHP 8.5.12 ext/xml and the
# source-built libxml2 2.15.4 (the same runtime build as the standard xml_parser_create_ns path).
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS vendor
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-xml unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs
# Packagist dist shasums are empty for these packages, so each Composer-installed package must equal the hashed
# GitHub archive of its locked commit.
RUN set -e; check() { \
        curl --fail --location --retry 3 "https://codeload.github.com/$2/legacy.zip/$3" --output "/work/archives/$1.zip"; \
        echo "$4  /work/archives/$1.zip" | sha256sum --check; \
        mkdir "/work/archives/$1" && unzip -q "/work/archives/$1.zip" -d "/work/archives/$1"; \
        diff -r /work/archives/$1/* "/work/vendor/$1"; \
    }; mkdir -p /work/archives/pear; \
    check pear/xml_parser pear/XML_Parser 0134baa2df2054afcca41e9307b98a21db84365d 0a814665499e110abfbe09950c5740d3f5b4929749fbf3c6fe766dc2f09bb581; \
    check pear/pear-core-minimal pear/pear-core-minimal c7b55789d01de0ce090d289b73f1bbd6a2f113b1 efb90a504f72e3c30b9345b7ce08e62984e6411e215285722c2a9027ed328374; \
    check pear/console_getopt pear/Console_Getopt a41f8d3e668987609178c7c4a9fe48fecac53fa0 b4eed79039bc4d20e59d540bb85396666445b8c6a6bd1bc04017cca49bd2169c; \
    check pear/pear_exception pear/PEAR_Exception b14fbe2ddb0b9f94f5b24cf08783d599f776fff0 6971a771990ae8081d2b0f1c2126447684e92ace553a9003e5651afec2e3f64d
RUN composer --version > /work/composer-version.txt

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

# Xdebug is built for the same runtime without LLVM instrumentation; it only records PHP line coverage.
FROM build AS xdebug
RUN apt-get update -qq && apt-get install -y --no-install-recommends autoconf && rm -rf /var/lib/apt/lists/*
WORKDIR /work/xdebug
RUN curl --fail --location --retry 3 https://pecl.php.net/get/xdebug-3.5.3.tgz --output /work/xdebug-3.5.3.tgz \
    && echo 'f073de91bea046106abf4d6071c963ea71e58571df6ce58948ceca89d121cb2d  /work/xdebug-3.5.3.tgz' | sha256sum --check \
    && tar -xzf /work/xdebug-3.5.3.tgz -C /work/xdebug
WORKDIR /work/xdebug/xdebug-3.5.3
RUN /opt/php/bin/phpize && CFLAGS='-O2 -g' LDFLAGS='' ./configure --with-php-config=/opt/php/bin/php-config --enable-xdebug \
    && make -j8 && cp modules/xdebug.so /work/xdebug.so \
    && /opt/php/bin/php -d zend_extension=/work/xdebug.so -r 'echo "Xdebug ", phpversion("xdebug"), PHP_EOL;' >> /work/toolchain.txt

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
COPY --from=build /work/licenses.txt /work/xml-sources.txt /work/
COPY --from=build /work/source/php-8.5.12/ext/xml /work/source/php-8.5.12/ext/xml
COPY --from=build /work/source/php-8.5.12/ext/libxml /work/source/php-8.5.12/ext/libxml
COPY --from=build /work/source/libxml2-2.15.4 /work/source/libxml2-2.15.4
COPY --from=xdebug /work/xdebug.so /work/xdebug.so
COPY --from=xdebug /work/toolchain.txt /work/toolchain.txt
COPY --from=vendor /work/vendor /work/vendor
COPY --from=vendor /work/composer-version.txt /work/composer-version.txt
# Xdebug is loaded but off by default; run-control.sh and queue replay switch it on with -d xdebug.mode=coverage.
RUN cat /work/composer-version.txt >> /work/toolchain.txt \
    && printf 'zend_extension=/work/xdebug.so\nxdebug.mode=off\n' > /opt/php/lib/php.ini \
    && /opt/php/bin/php -r 'exit(phpversion("xdebug") === "3.5.3" ? 0 : 1);'
COPY harness.php summary.php fuzz-target.php run-control.php run-control.py run-control.sh target.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
