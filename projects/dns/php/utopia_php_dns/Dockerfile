FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-intl php8.5-mbstring unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs \
    && curl --fail --location --retry 3 https://codeload.github.com/utopia-php/dns/legacy.zip/59f42a9fb33247e1e0c1f8f7e31ff056185d05a3 --output /work/parser-source.zip \
    && echo '946fcc63862df4f04c3aa3eb9c25ef4a9bac84968611a0c179dd007166f8f536  /work/parser-source.zip' | sha256sum --check \
    && mkdir /work/parser-source && cd /work/parser-source && unzip -q /work/parser-source.zip \
    && diff -r /work/parser-source/utopia-php-dns-59f42a9/src /work/vendor/utopia-php/dns/src \
    && grep -q 'Permission is hereby granted' /work/vendor/utopia-php/dns/LICENSE
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
