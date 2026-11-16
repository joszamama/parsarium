FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-interaction --no-progress --prefer-dist \
    && mkdir -p /work/parser \
    && curl --fail --location --retry 3 \
       https://raw.githubusercontent.com/collectiveaccess/pawtucket2/2.0.12/app/lib/Parsers/PlyToStl.php \
       --output /work/parser/PlyToStl.php \
    && echo 'ad0176a247a6cdc3d4e7a816520e332427e6066385ba483c239aefbc43d15a18  /work/parser/PlyToStl.php' | sha256sum --check
RUN { php --version | head -1; composer --version; } > /work/toolchain.txt
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-xdebug && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
COPY --from=build /work/parser /work/parser
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY support /work/support
COPY harness.php fuzz-target.php run-control.php /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/run-control.php"]
