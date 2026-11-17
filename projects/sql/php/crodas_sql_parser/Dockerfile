FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-intl php8.5-mbstring unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs \
    && curl --fail --location --retry 3 https://codeload.github.com/crodas/SQLParser/legacy.zip/a0241cb8755ed36b2a0d0812503ee71abfbe52ac --output /work/parser-source.zip \
    && echo 'cfcf15a23ea58c8891b38d092b05833896ead8cd58b6c0f4afb5a600954c64fa  /work/parser-source.zip' | sha256sum --check \
    && mkdir /work/parser-source && cd /work/parser-source && unzip -q /work/parser-source.zip \
    && diff -r /work/parser-source/crodas-SQLParser-a0241cb/src /work/vendor/crodas/sql-parser/src \
    && echo 'eceb1a17a8879328c39d3bae290bbfc485007a788aa1ef7b4a92480b059846e8  /work/parser-source/crodas-SQLParser-a0241cb/LICENSE' | sha256sum --check
RUN { php --version | head -1; composer --version; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-intl php8.5-mbstring php8.5-xdebug \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.php fuzz-target.php run-control.php replay.php target.json /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/run-control.php"]
