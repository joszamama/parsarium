FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-intl php8.5-mbstring unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs \
    && curl --fail --location --retry 3 https://codeload.github.com/joelwurtz/php-json-stream-polyfill/legacy.zip/0136c414d2100f779dffd8910e5d591f97845004 --output /work/parser-source.zip \
    && echo '01b0b9aeebd069e236191cb89868f9a9cdf48c670cdeafc19e197a16a255490d  /work/parser-source.zip' | sha256sum --check \
    && mkdir /work/parser-source && cd /work/parser-source && unzip -q /work/parser-source.zip \
    && diff -r /work/parser-source/joelwurtz-php-json-stream-polyfill-0136c41/src /work/vendor/joelwurtz/json-stream-polyfill/src \
    && cmp /work/parser-source/joelwurtz-php-json-stream-polyfill-0136c41/bootstrap.php /work/vendor/joelwurtz/json-stream-polyfill/bootstrap.php
# Composer "files" autoload would load the polyfill before php-fuzzer installs its include
# instrumentation. Drop only that loader entry; harness.php requires the README-documented
# bootstrap.php itself after vendor/autoload.php. Package source is unchanged.
RUN grep -q "/joelwurtz/json-stream-polyfill/bootstrap.php'," /work/vendor/composer/autoload_files.php \
    && grep -q "/joelwurtz/json-stream-polyfill/bootstrap.php'," /work/vendor/composer/autoload_static.php \
    && sed -i "\#/joelwurtz/json-stream-polyfill/bootstrap.php',#d" \
       /work/vendor/composer/autoload_files.php /work/vendor/composer/autoload_static.php \
    && ! grep -rq "json-stream-polyfill" /work/vendor/composer/autoload_files.php /work/vendor/composer/autoload_static.php \
    && php -r 'require "/work/vendor/autoload.php"; exit(function_exists("json_stream_decode") ? 1 : 0);'
RUN { php --version | head -1; composer --version; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-intl php8.5-mbstring php8.5-xdebug \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.php fuzz-target.php run-control.php target.json /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/run-control.php"]
