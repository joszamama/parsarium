FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-intl php8.5-mbstring unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs \
    && curl --fail --location --retry 3 https://codeload.github.com/soundintheory/php-sql-parser/legacy.zip/dcb81216a13be124d21711b8fefb6e80db7af472 --output /work/parser-source.zip \
    && echo '75d3ea13ba4238d034b49eeff7b995bde4a6539e63054b95da2d31b69937cbb6  /work/parser-source.zip' | sha256sum --check \
    && mkdir /work/parser-source && cd /work/parser-source && unzip -q /work/parser-source.zip \
    && diff -r /work/parser-source/soundintheory-php-sql-parser-dcb8121/src /work/vendor/soundintheory/php-sql-parser/src \
    && echo 'e8d39df1315f5185bf0f22fcc5bf9f2b3d6ad3f74bfba735f2cb4b34b51f4d6e  /work/parser-source/soundintheory-php-sql-parser-dcb8121/src/PHPSQL/Parser.php' | sha256sum --check \
    && echo '0e8e12895f3bb887151ff02562a326d53c0eb1ef3a8454517e1a60ecc2fe4781  /work/parser-source/soundintheory-php-sql-parser-dcb8121/composer.json' | sha256sum --check
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
