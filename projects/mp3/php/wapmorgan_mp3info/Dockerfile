FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-mbstring unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-interaction --no-progress --prefer-dist \
    && curl --fail --location --retry 3 \
       https://api.github.com/repos/wapmorgan/Mp3Info/zipball/e532c2e1997874f9c672c7810ce90ef15004ef94 \
       --output /work/mp3info-0.1.1.zip \
    && echo '12bb890854c39b6410a7e81e4d8f102ee73ef33589abc832bda9c9dac04f57f6  /work/mp3info-0.1.1.zip' | sha256sum --check \
    && unzip -q /work/mp3info-0.1.1.zip -d /work/archive \
    && diff -r /work/archive/wapmorgan-Mp3Info-e532c2e /work/vendor/wapmorgan/mp3info
RUN { php --version | head -1; composer --version; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-mbstring php8.5-xdebug \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.php replay.php fuzz-target.php run-control.php /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/run-control.php"]
