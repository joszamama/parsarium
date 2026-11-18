FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-intl php8.5-mbstring unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs \
    && curl --fail --location --retry 3 https://codeload.github.com/kwasii1/laravel-sql-parser/legacy.zip/17aa576c47feb38ef3b66b11d0cca449730f7b96 --output /work/parser-source.zip \
    && echo '9c1bb198aceb536fb1d415012ae6b7b6a5407a12e71dbe88d5a0c9c2c86935f9  /work/parser-source.zip' | sha256sum --check \
    && mkdir /work/parser-source && cd /work/parser-source && unzip -q /work/parser-source.zip \
    && diff -r /work/parser-source/kwasii1-laravel-sql-parser-17aa576/src /work/vendor/kwasii/laravel-sql-parser/src \
    && echo '91457e43f9cd0d3ff941944bd756371faeeaedd0db7c5fee4b097d1750d54ba1  /work/parser-source/kwasii1-laravel-sql-parser-17aa576/LICENSE.md' | sha256sum --check
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
