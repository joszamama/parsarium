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
       https://raw.githubusercontent.com/ArchiveHeritageGroup/heratio/v1.165.35/packages/ahg-3d-model/src/Services/ModelMetadataExtractor.php \
       --output /work/parser/ModelMetadataExtractor.php \
    && echo '6183477dfb064f92b008ae85c359200c6de69294f70ac624cb4c515b19562439  /work/parser/ModelMetadataExtractor.php' | sha256sum --check
RUN { php --version | head -1; composer --version; } > /work/toolchain.txt
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-xdebug && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
COPY --from=build /work/parser /work/parser
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.php fuzz-target.php run-control.php /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/run-control.php"]
