FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-mbstring unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
# Composer records no dist shasum, so the installed source is diffed against the hash-pinned archive.
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs \
    && curl --fail --location --retry 3 https://codeload.github.com/colinodell/json5/legacy.zip/5724d21bc5c910c2560af1b8915f0cc0163579c8 --output /work/parser-source.zip \
    && echo '919081aebb1a403327b833331d09b56a51ee90ccaee0f884ecd19427f5dfc858  /work/parser-source.zip' | sha256sum --check \
    && unzip -q /work/parser-source.zip -d /work/archive \
    && diff -r /work/archive/colinodell-json5-5724d21/src /work/vendor/colinodell/json5/src \
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
