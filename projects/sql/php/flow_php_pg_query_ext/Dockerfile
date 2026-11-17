# flow-php/pg-query-ext 0.48.0 (PIE package php-ext on Packagist) is the pg_query PHP extension: ext/pg_query.c
# links libpg_query 18.0.0 statically, and pg_query_parse() returns libpg_query's JSON parse tree. The image builds
# PHP 8.5.12 (--disable-all) without coverage, then libpg_query and the extension with Clang/LLVM source coverage,
# so llvm-cov reports ext/pg_query.c and libpg_query lines from pg_query.so.
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    autoconf ca-certificates clang curl libclang-rt-21-dev libprotobuf-c-dev llvm make pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# The Packagist dist of pg-query-ext 0.48.0 is the GitHub archive of its locked commit (a subtree split of the
# flow-php/flow monorepo). The split has no LICENSE file; the monorepo LICENSE at the 0.48.0 tag (MIT) is pinned.
# The extension pins libpg_query 18.0.0 in config.m4; bison/flex #line directives in gram.c and scan.c point to
# gram.y and scan.l, which are not shipped, so they are removed and coverage maps to the pinned C files.
RUN curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/pganalyze/libpg_query/tar.gz/refs/tags/18.0.0 --output /work/libpg_query-18.0.0.tar.gz \
    && echo '6ad7783f272acfd116455c66a03298a0cac9a9168281df547969219112f0260f  /work/libpg_query-18.0.0.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/flow-php/pg-query-ext/tar.gz/283a87e05cca599534c9c372935a60d369590a08 --output /work/parser-source.tar.gz \
    && echo '6f984b73d57b777c240bd59e31a7f46cee03ca5e984124bc25ea57379de5b16f  /work/parser-source.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://raw.githubusercontent.com/flow-php/flow/1679ceb4eefb7556a5d40f61c6bbaf2936d57b2a/LICENSE --output /work/flow-LICENSE \
    && echo 'eeb68d50be5e8cf87b1ba5fa5cff838d988dbf5f936491b191758bec3b9decc6  /work/flow-LICENSE' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source && tar -xzf /work/libpg_query-18.0.0.tar.gz -C /work/source \
    && tar -xzf /work/parser-source.tar.gz -C /work/source \
    && mv /work/source/pg-query-ext-283a87e05cca599534c9c372935a60d369590a08 /work/source/pg-query-ext-0.48.0 \
    && cp /work/flow-LICENSE /work/source/pg-query-ext-0.48.0/LICENSE.flow-monorepo \
    && grep -qx 'describe-name: 0.48.0' /work/source/pg-query-ext-0.48.0/.git_archival.txt \
    && grep -q 'LIBPG_QUERY_VERSION="18.0.0"' /work/source/pg-query-ext-0.48.0/ext/config.m4 \
    && grep -q 'Redistribution and use in source and binary forms' /work/source/libpg_query-18.0.0/LICENSE \
    && sed -i '/^#line /d' /work/source/libpg_query-18.0.0/src/postgres/src_backend_parser_gram.c /work/source/libpg_query-18.0.0/src/postgres/src_backend_parser_scan.c \
    && cd /work/source && sha256sum php-8.5.12/LICENSE pg-query-ext-0.48.0/LICENSE.flow-monorepo libpg_query-18.0.0/LICENSE > /work/licenses.txt \
    && sha256sum pg-query-ext-0.48.0/ext/pg_query.c pg-query-ext-0.48.0/ext/php_pg_query.h pg-query-ext-0.48.0/ext/pg_query_arginfo.h pg-query-ext-0.48.0/ext/config.m4 > /work/pg-query-ext-sources.txt
WORKDIR /work/source/php-8.5.12
RUN CC=clang CXX=clang++ CFLAGS='-O1 -g' ./configure --prefix=/opt/php --enable-cli --disable-all --without-pcre-jit \
    || { tail -40 config.log; exit 1; } \
    && make -j8 && make install
WORKDIR /work/source/libpg_query-18.0.0
RUN make -j8 CC=clang CFLAGS='-fprofile-instr-generate -fcoverage-mapping' build
ENV CC=clang CFLAGS='-O0 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate'
WORKDIR /work/source/pg-query-ext-0.48.0/ext
RUN /opt/php/bin/phpize && ./configure --with-php-config=/opt/php/bin/php-config --with-pg-query=/work/source/libpg_query-18.0.0 \
    && make -j8 && make install \
    && printf 'extension=pg_query.so\n' > /opt/php/lib/php.ini \
    && LLVM_PROFILE_FILE=/tmp/build-%m.profraw /opt/php/bin/php -r 'exit(phpversion("pg_query") === "0.48.0" ? 0 : 1);'
RUN { LLVM_PROFILE_FILE=/tmp/build-%m.profraw sh -c \
        '/opt/php/bin/php -v | head -1; /opt/php/bin/php -r "echo \"pg_query \", phpversion(\"pg_query\"), PHP_EOL;"; /opt/php/bin/php --ri pg_query | grep -i "libpg_query version"'; \
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
COPY --from=build /work/toolchain.txt /work/licenses.txt /work/pg-query-ext-sources.txt /work/
COPY --from=build /work/source/pg-query-ext-0.48.0/ext /work/source/pg-query-ext-0.48.0/ext
COPY --from=build /work/source/libpg_query-18.0.0/src /work/source/libpg_query-18.0.0/src
COPY --from=build /work/source/libpg_query-18.0.0/vendor /work/source/libpg_query-18.0.0/vendor
COPY --from=build /work/source/libpg_query-18.0.0/protobuf /work/source/libpg_query-18.0.0/protobuf
COPY summary.php harness.php fuzz-target.php run-control.py run-control.sh target.json /work/
RUN chmod +x /work/fuzz-target.php
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
