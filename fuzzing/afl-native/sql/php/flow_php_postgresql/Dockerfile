# AFL++ instruments the native parse path behind flow-php/postgresql's sql_parse(): pg-query-ext 0.48.0
# ext/pg_query.c (pg_query_parse_protobuf) and libpg_query 18.0.0 src_backend_parser_gram.c, src_backend_parser_scan.c
# and src_backend_parser_parser.c, while the same PHP process decodes the protobuf tree into the package AST classes
# with google/protobuf. The PHP runtime is compiled with afl-clang-fast under an allowlist that matches no PHP
# source. The package's own PHP lines are recorded separately by /work/afl_trace (Xdebug 3.5.3 from the base image,
# loaded only for that trace), which scripts/verify_sql_feedback.py reads as parser source features.
FROM --platform=linux/arm64 parsarium/sql-php-flow_php_postgresql:local AS base

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 autoconf ca-certificates clang curl libprotobuf-c-dev llvm make pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/pganalyze/libpg_query/tar.gz/refs/tags/18.0.0 --output /work/libpg_query-18.0.0.tar.gz \
    && echo '6ad7783f272acfd116455c66a03298a0cac9a9168281df547969219112f0260f  /work/libpg_query-18.0.0.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/flow-php/pg-query-ext/tar.gz/283a87e05cca599534c9c372935a60d369590a08 --output /work/pg-query-ext.tar.gz \
    && echo '6f984b73d57b777c240bd59e31a7f46cee03ca5e984124bc25ea57379de5b16f  /work/pg-query-ext.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source && tar -xzf /work/libpg_query-18.0.0.tar.gz -C /work/source \
    && tar -xzf /work/pg-query-ext.tar.gz -C /work/source \
    && mv /work/source/pg-query-ext-283a87e05cca599534c9c372935a60d369590a08 /work/source/pg-query-ext-0.48.0 \
    && sed -i '/^#line /d' /work/source/libpg_query-18.0.0/src/postgres/src_backend_parser_gram.c /work/source/libpg_query-18.0.0/src/postgres/src_backend_parser_scan.c \
    && cd /work/source && sha256sum php-8.5.12/LICENSE libpg_query-18.0.0/LICENSE > /work/licenses.txt \
    && sha256sum pg-query-ext-0.48.0/ext/pg_query.c pg-query-ext-0.48.0/ext/php_pg_query.h pg-query-ext-0.48.0/ext/pg_query_arginfo.h pg-query-ext-0.48.0/ext/config.m4 > /work/pg-query-ext-sources.txt
WORKDIR /work/source/php-8.5.12
RUN printf 'src:parsarium-no-php-source.c\n' > /work/afl-allowlist-php.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt CC=afl-clang-fast CXX=afl-clang-fast++ CFLAGS='-O1 -g' \
    ./configure --prefix=/opt/php --enable-cli --disable-all --enable-ctype --without-pcre-jit \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt make -j8 && make install
# libpg_query compiles its sources as src/postgres/<file>.c; each suffix entry names exactly one file
# (src_backend_parser_scan.c does not match src_backend_parser_scansup.c).
WORKDIR /work/source/libpg_query-18.0.0
RUN printf 'src:src/postgres/src_backend_parser_gram.c\nsrc:src/postgres/src_backend_parser_scan.c\nsrc:src/postgres/src_backend_parser_parser.c\n' > /work/afl-allowlist-libpg_query.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-libpg_query.txt make -j8 CC=afl-clang-fast build
WORKDIR /work/source/pg-query-ext-0.48.0/ext
RUN printf 'src:pg-query-ext-0.48.0/ext/pg_query.c\n' > /work/afl-allowlist-pg-query-ext.txt
RUN /opt/php/bin/phpize && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-pg-query-ext.txt CC=afl-clang-fast CFLAGS='-O1 -g' \
    ./configure --with-php-config=/opt/php/bin/php-config --with-pg-query=/work/source/libpg_query-18.0.0 \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-pg-query-ext.txt make -j8 && make install
RUN cd /work/source && for object in $(find php-8.5.12 libpg_query-18.0.0 pg-query-ext-0.48.0 -name '*.o' | sort); do \
        if nm "$object" | grep -q __afl_area_ptr; then echo "$object"; fi; \
    done > /work/afl-instrumented-objects.txt && cat /work/afl-instrumented-objects.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb libprotobuf-c1 \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/php /opt/php
COPY --from=build /work/afl-allowlist-php.txt /work/afl-allowlist-libpg_query.txt /work/afl-allowlist-pg-query-ext.txt /work/afl-instrumented-objects.txt /work/licenses.txt /work/pg-query-ext-sources.txt /work/
COPY --from=base /work/vendor /work/vendor
COPY --from=base /work/xdebug.so /work/xdebug.so
RUN printf 'extension=pg_query.so\n' > /opt/php/lib/php.ini
COPY projects/sql/php/flow_php_postgresql/fuzz-target.php projects/sql/php/flow_php_postgresql/harness.php projects/sql/php/flow_php_postgresql/summary.php fuzzing/afl-native/sql/php/flow_php_postgresql/afl_trace fuzzing/afl-native/sql/php/flow_php_postgresql/afl_trace.php /work/
RUN chmod +x /work/fuzz-target.php
ENTRYPOINT ["/work/fuzz-target.php"]
