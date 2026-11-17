FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-xml unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
# Composer records no dist shasum, so the installed package is diffed against the hash-pinned archive.
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs \
    && curl --fail --location --retry 3 https://codeload.github.com/jtrumbull/xml-parser/legacy.zip/94212d1bfc304ba9ac0a50b14e0a0cf67c877e86 --output /work/parser-source.zip \
    && echo '19b2ab9a913f4e814bff5ad0de01158e6a49cc896619bc3324dd5b72e9b85d77  /work/parser-source.zip' | sha256sum --check \
    && unzip -q /work/parser-source.zip -d /work/archive \
    && diff -r /work/archive/jtrumbull-xml-parser-94212d1 /work/vendor/jtrumbull/xml-parser \
    && rm -rf /work/archive
RUN { php --version | head -1; php -r 'echo "libxml ", LIBXML_DOTTED_VERSION, PHP_EOL;'; composer --version; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-xml php8.5-xdebug \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY probe.php /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/probe.php"]
