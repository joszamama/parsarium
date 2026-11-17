# flow-php/postgresql 0.48.0 parses SQL through sql_parse()/Parser::parse(): the pg_query extension
# (flow-php/pg-query-ext 0.48.0 over libpg_query 18.0.0) returns a protobuf parse tree that the package decodes into
# its generated AST classes with google/protobuf, and the package Traverser walks that tree. The image pairs two
# coverage sources on one run: Xdebug line coverage for the package PHP source and Clang/LLVM source coverage of
# ext/pg_query.c and libpg_query linked into pg_query.so (the same native build as the pg-query-ext path).
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS vendor
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli unzip \
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
    }; mkdir -p /work/archives/flow-php /work/archives/google /work/archives/psr /work/archives/symfony; \
    check flow-php/postgresql flow-php/postgresql f28a5e598000b42a7c6c465ab4b7a1b9b8ed5984 31f8f0d3f67c2c1c8907ce5591fbfd6f5738fa6161c22018251d25a886cd99b2; \
    check flow-php/telemetry flow-php/telemetry 4618491c4fe0f832052008789d8c85b19d210b1f 6b10ca31eded8472841af28d42e803199b53361e801ef12ccab75e2ae6ee6058; \
    check flow-php/types flow-php/types 7f9189240217b3f4dceebbdeefbd6a5cdc97a6d3 603307443a02c1f2a9054c89670adf91d8c8c9c77eb646d8d459f4530113bb00; \
    check google/protobuf protocolbuffers/protobuf-php 020bc8e831611869ac387ddd38fbbadd78d15195 1a7e76eba86eec39cd9d6b2dbfcb4c5d11f6a724b65f6792b8e7fe8a748aa378; \
    check psr/clock php-fig/clock e41a24703d4560fd0acb709162f73b8adfc3aa0d 72a2682083efc51108e5d7d0e880d45d85236100692c86d093c3f6f9205ae573; \
    check symfony/polyfill-mbstring symfony/polyfill-mbstring 122889ed24dc000165bcbfd77ec412f15cbdfc6a 560bc33ca56b79d9c285d9a2f14058ac489b6e6341df75c4e49cf87434c6e3ce; \
    sha256sum /work/vendor/flow-php/postgresql/LICENSE /work/vendor/google/protobuf/LICENSE > /work/package-licenses.txt
RUN composer --version > /work/composer-version.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    autoconf ca-certificates clang curl libclang-rt-21-dev libprotobuf-c-dev llvm make pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Same pinned extension, libpg_query and PHP sources as projects/sql/php/flow_php_pg_query_ext.
RUN curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/pganalyze/libpg_query/tar.gz/refs/tags/18.0.0 --output /work/libpg_query-18.0.0.tar.gz \
    && echo '6ad7783f272acfd116455c66a03298a0cac9a9168281df547969219112f0260f  /work/libpg_query-18.0.0.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/flow-php/pg-query-ext/tar.gz/283a87e05cca599534c9c372935a60d369590a08 --output /work/pg-query-ext.tar.gz \
    && echo '6f984b73d57b777c240bd59e31a7f46cee03ca5e984124bc25ea57379de5b16f  /work/pg-query-ext.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source && tar -xzf /work/libpg_query-18.0.0.tar.gz -C /work/source \
    && tar -xzf /work/pg-query-ext.tar.gz -C /work/source \
    && mv /work/source/pg-query-ext-283a87e05cca599534c9c372935a60d369590a08 /work/source/pg-query-ext-0.48.0 \
    && grep -qx 'describe-name: 0.48.0' /work/source/pg-query-ext-0.48.0/.git_archival.txt \
    && sed -i '/^#line /d' /work/source/libpg_query-18.0.0/src/postgres/src_backend_parser_gram.c /work/source/libpg_query-18.0.0/src/postgres/src_backend_parser_scan.c \
    && cd /work/source && sha256sum php-8.5.12/LICENSE libpg_query-18.0.0/LICENSE > /work/licenses.txt \
    && sha256sum pg-query-ext-0.48.0/ext/pg_query.c pg-query-ext-0.48.0/ext/php_pg_query.h pg-query-ext-0.48.0/ext/pg_query_arginfo.h pg-query-ext-0.48.0/ext/config.m4 > /work/pg-query-ext-sources.txt
# google/protobuf's pure-PHP runtime calls ctype_upper() while it builds the descriptor pool.
WORKDIR /work/source/php-8.5.12
RUN CC=clang CXX=clang++ CFLAGS='-O1 -g' ./configure --prefix=/opt/php --enable-cli --disable-all --enable-ctype --without-pcre-jit \
    || { tail -40 config.log; exit 1; } \
    && make -j8 && make install
WORKDIR /work/source/libpg_query-18.0.0
RUN make -j8 CC=clang CFLAGS='-fprofile-instr-generate -fcoverage-mapping' build
WORKDIR /work/source/pg-query-ext-0.48.0/ext
RUN /opt/php/bin/phpize && CC=clang CFLAGS='-O0 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
    ./configure --with-php-config=/opt/php/bin/php-config --with-pg-query=/work/source/libpg_query-18.0.0 \
    && make -j8 && make install

# Xdebug is built for the same runtime without LLVM instrumentation; it only records PHP line coverage.
FROM build AS xdebug
WORKDIR /work/xdebug
RUN curl --fail --location --retry 3 https://pecl.php.net/get/xdebug-3.5.3.tgz --output /work/xdebug-3.5.3.tgz \
    && echo 'f073de91bea046106abf4d6071c963ea71e58571df6ce58948ceca89d121cb2d  /work/xdebug-3.5.3.tgz' | sha256sum --check \
    && tar -xzf /work/xdebug-3.5.3.tgz -C /work/xdebug
WORKDIR /work/xdebug/xdebug-3.5.3
RUN /opt/php/bin/phpize && CC=clang CFLAGS='-O2 -g' LDFLAGS='' ./configure --with-php-config=/opt/php/bin/php-config --enable-xdebug \
    && make -j8 && cp modules/xdebug.so /work/xdebug.so
RUN { LLVM_PROFILE_FILE=/tmp/build-%m.profraw sh -c \
        '/opt/php/bin/php -v | head -1; /opt/php/bin/php -d extension=pg_query.so -r "echo \"pg_query \", phpversion(\"pg_query\"), PHP_EOL;"; /opt/php/bin/php -d extension=pg_query.so --ri pg_query | grep -i "libpg_query version"; /opt/php/bin/php -d zend_extension=/work/xdebug.so -r "echo \"Xdebug \", phpversion(\"xdebug\"), PHP_EOL;"'; \
      clang --version | head -1; } > /work/toolchain.txt && rm -f /tmp/build-*.profraw

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb libprotobuf-c1 llvm python3 \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
# Runs outside run-control.sh (replay, fuzz smoke) keep the extension's LLVM profile on the writable tmpfs.
ENV LLVM_PROFILE_FILE=/tmp/parsarium-%m.profraw
WORKDIR /work
COPY --from=build /opt/php /opt/php
COPY --from=build /work/licenses.txt /work/pg-query-ext-sources.txt /work/
COPY --from=build /work/source/pg-query-ext-0.48.0/ext /work/source/pg-query-ext-0.48.0/ext
COPY --from=build /work/source/libpg_query-18.0.0/src /work/source/libpg_query-18.0.0/src
COPY --from=build /work/source/libpg_query-18.0.0/vendor /work/source/libpg_query-18.0.0/vendor
COPY --from=build /work/source/libpg_query-18.0.0/protobuf /work/source/libpg_query-18.0.0/protobuf
COPY --from=xdebug /work/xdebug.so /work/xdebug.so
COPY --from=xdebug /work/toolchain.txt /work/toolchain.txt
COPY --from=vendor /work/vendor /work/vendor
COPY --from=vendor /work/composer-version.txt /work/package-licenses.txt /work/
# Xdebug is loaded but off by default; run-control.sh switches it on with -d xdebug.mode=coverage.
RUN cat /work/composer-version.txt >> /work/toolchain.txt \
    && printf 'extension=pg_query.so\nzend_extension=/work/xdebug.so\nxdebug.mode=off\n' > /opt/php/lib/php.ini \
    && LLVM_PROFILE_FILE=/tmp/check-%m.profraw /opt/php/bin/php -r 'exit(phpversion("xdebug") === "3.5.3" && phpversion("pg_query") === "0.48.0" ? 0 : 1);' \
    && rm -f /tmp/check-*.profraw
COPY summary.php harness.php fuzz-target.php run-control.php run-control.py run-control.sh target.json /work/
RUN chmod +x /work/fuzz-target.php
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
