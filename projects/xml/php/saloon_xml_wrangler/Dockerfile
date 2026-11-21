FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive COMPOSER_ALLOW_SUPERUSER=1
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates composer curl php8.5-cli php8.5-xml unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-plugins --no-interaction --no-progress --prefer-dist --ignore-platform-reqs
# Each Composer-installed package must equal the hashed GitHub archive of its locked commit.
RUN set -e; check() { \
        curl --fail --location --retry 3 "https://codeload.github.com/$2/legacy.zip/$3" --output "/work/archives/$1.zip"; \
        echo "$4  /work/archives/$1.zip" | sha256sum --check; \
        mkdir "/work/archives/$1" && unzip -q "/work/archives/$1.zip" -d "/work/archives/$1"; \
        diff -r /work/archives/$1/* "/work/vendor/$1"; \
    }; mkdir -p /work/archives/saloonphp /work/archives/veewee /work/archives/php-standard-library \
        /work/archives/revolt /work/archives/spatie /work/archives/webmozart; \
    check saloonphp/xml-wrangler saloonphp/xml-wrangler 4f35b68245dee8041193369efd4d73a98ad04a5f 7951d70994f5df00b173d4ee851be0b47ed6ac05f72594e005b7261f3a3abb38; \
    check veewee/xml veewee/xml a3e60ccda54a3326f444fe7a30916da3523d3844 37d8933c93b7f1f2ee277cf2619326282c329e914d99c2bace7d346a11f6339f; \
    check php-standard-library/php-standard-library php-standard-library/php-standard-library f537759b58ba36c8093505004e1bff7578238736 ac95b7661cf57380c26f04aceeff5702857f55e64aa7769f3e84c151326f35e5; \
    check revolt/event-loop revoltphp/event-loop 44061cf513e53c6200372fc935ac42271566295d 8b80136b01aee8ee3d5fe28e7de96bda9f70b6c3bd11d6bd08dec3bd5c112816; \
    check spatie/array-to-xml spatie/array-to-xml 88b2f3852a922dd73177a68938f8eb2ec70c7224 df47ac43697ee6408d035a82d8e9d075e577793159eb3baa7f4dbd939d41eebc; \
    check webmozart/assert webmozarts/assert 9be6926d8b485f55b9229203f962b51ed377ba68 80dc9ac0ae041cdf0503e40bb1bc96a57f09c21ec0d076e68d2f75f946f80a05
RUN { php --version | head -1; composer --version; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
# php-standard-library/str (Psl\Str\uppercase, used when veewee/xml formats a libxml issue) requires ext-mbstring.
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-xml php8.5-mbstring php8.5-xdebug \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
COPY --from=build /work/toolchain.txt /work/toolchain.txt
RUN php -r 'echo "libxml ", LIBXML_DOTTED_VERSION, PHP_EOL;' >> /work/toolchain.txt
COPY harness.php summary.php fuzz-target.php run-control.php target.json /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/run-control.php"]
