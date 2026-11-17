FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-mbstring unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
# Composer records no dist shasum, so the installed source is diffed against the hash-pinned archive.
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs \
    && curl --fail --location --retry 3 https://codeload.github.com/prewk/xml-string-streamer/legacy.zip/a1f4a5250d548d06fd385fa86241c0c2d7d607fd --output /work/parser-source.zip \
    && echo 'f652cf058971933b499858ff9439fa4cef424a9377dad09218d8ddb80ee297ed  /work/parser-source.zip' | sha256sum --check \
    && unzip -q /work/parser-source.zip -d /work/archive \
    && diff -r /work/archive/prewk-xml-string-streamer-a1f4a52/src /work/vendor/prewk/xml-string-streamer/src \
    && rm -rf /work/archive
RUN { php --version | head -1; composer --version; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-mbstring php8.5-xdebug \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY probe.php /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/probe.php"]
