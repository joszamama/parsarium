FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-mbstring unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
# Composer records no dist shasum, so the installed source is diffed against the hash-pinned archive.
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs \
    && curl --fail --location --retry 3 https://codeload.github.com/zendframework/zend-json/legacy.zip/e9ddb1192d93fe7fff846ac895249c39db75132b --output /work/parser-source.zip \
    && echo 'c7f83996835481a6024b770aa30f1f89f9b9fb66e1566890de1a299c4d45206b  /work/parser-source.zip' | sha256sum --check \
    && unzip -q /work/parser-source.zip -d /work/archive \
    && diff -r /work/archive/zendframework-zend-json-e9ddb11/src /work/vendor/zendframework/zend-json/src \
    && rm -rf /work/archive /work/parser-source.zip
# laminas/laminas-json conflicts with zendframework/zend-json in Composer, so the verified successor
# release (same archive hash as projects/json/php/laminas_json/source-lock.json) is unpacked beside it.
RUN curl --fail --location --retry 3 https://codeload.github.com/laminas/laminas-json/legacy.zip/5448d357c4520d79f5caf4d46a1fe03ec8b8e4b0 --output /work/laminas-source.zip \
    && echo '5b5cf97123f3ef5db4fb5229ff44c6620523e16734ae8526e51550ca5c05ac9c  /work/laminas-source.zip' | sha256sum --check \
    && unzip -q /work/laminas-source.zip -d /work/archive \
    && mv /work/archive/laminas-laminas-json-5448d35 /work/laminas-json \
    && rm -rf /work/archive /work/laminas-source.zip
RUN { php --version | head -1; composer --version; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-mbstring php8.5-xdebug \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
COPY --from=build /work/laminas-json/src /work/laminas-json/src
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY probe.php /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/probe.php"]
