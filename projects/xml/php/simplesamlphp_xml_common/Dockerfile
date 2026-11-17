FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/simplesamlphp/xml-common/legacy.zip/c50b33dfc4384c772e921c6072bded9b67081c03 --output /work/simplesamlphp-xml-common.zip \
    && echo '99a309a70d7c481ce6b707c3e56299629dc50e61955f35c459f1f64c9b07bf6c  /work/simplesamlphp-xml-common.zip' | sha256sum --check \
    && rm -rf /work/x && unzip -q /work/simplesamlphp-xml-common.zip -d /work/x \
    && mkdir -p /work/vendor/simplesamlphp && mv /work/x/simplesamlphp-* /work/vendor/simplesamlphp/xml-common \
    && echo '20c17d8b8c48a600800dfd14f95d5cb9ff47066a9641ddeab48dc54aec96e331  /work/vendor/simplesamlphp/xml-common/LICENSE' | sha256sum --check \
    && echo '0bee113cebaa1efddb4f6b1fb5f07c1fd2d3df262534eed622bcc5d3015ecd66  /work/vendor/simplesamlphp/xml-common/composer.json' | sha256sum --check \
    && echo '66c9fc061682207136d843d29d09b8e6800ddf95546b123d314f6bf27ba233f8  /work/vendor/simplesamlphp/xml-common/src/XML/DOMDocumentFactory.php' | sha256sum --check \
    && echo '00f511e99a9360b284bed289ea1facd4b2f2744a4bfaa81da63bda60399595a5  /work/vendor/simplesamlphp/xml-common/src/XML/Assert/Assert.php' | sha256sum --check
RUN curl --fail --location --retry 3 https://codeload.github.com/simplesamlphp/assert/legacy.zip/33dcdeac629fa84a049f63738c30ecebdcb53061 --output /work/simplesamlphp-assert.zip \
    && echo '8caf9c764fa80a5e05a814bd83e220d87475575295c01a78d1c8a8edbe53ed16  /work/simplesamlphp-assert.zip' | sha256sum --check \
    && rm -rf /work/x && unzip -q /work/simplesamlphp-assert.zip -d /work/x \
    && mkdir -p /work/vendor/simplesamlphp && mv /work/x/simplesamlphp-* /work/vendor/simplesamlphp/assert \
    && echo '20c17d8b8c48a600800dfd14f95d5cb9ff47066a9641ddeab48dc54aec96e331  /work/vendor/simplesamlphp/assert/LICENSE' | sha256sum --check \
    && echo 'a71096adba1f3da589d2c0e2f3391bb0705bbac4d3ffd53a25582f53bde18c1b  /work/vendor/simplesamlphp/assert/composer.json' | sha256sum --check \
    && echo 'd859717ba0ed4f83faa30a0edc43831f57704b9db901e332902559d05e6c7a87  /work/vendor/simplesamlphp/assert/src/Assert.php' | sha256sum --check
RUN curl --fail --location --retry 3 https://codeload.github.com/webmozarts/assert/legacy.zip/ff31ad6efc62e66e518fbab1cde3453d389bcdc8 --output /work/webmozart-assert.zip \
    && echo '23059de8c31f3c16f9c8b3e10a4b5394464aae2b2a06bb223c90846029c92b4f  /work/webmozart-assert.zip' | sha256sum --check \
    && rm -rf /work/x && unzip -q /work/webmozart-assert.zip -d /work/x \
    && mkdir -p /work/vendor/webmozart && mv /work/x/webmozarts-* /work/vendor/webmozart/assert \
    && echo '5f82f5e664e8683e3d97d3bec6f74620b9d0a4d8669f9e617da96bce8767d4d3  /work/vendor/webmozart/assert/LICENSE' | sha256sum --check \
    && echo '93a39bdca52a5f0f56b7071f59060dde8e2f4f6f45a3073728e8d58f1435a899  /work/vendor/webmozart/assert/composer.json' | sha256sum --check \
    && echo '7cb6138a125b4a3c62d4dcac3a855e608f4545a911cb53ff9426c3ad20464c88  /work/vendor/webmozart/assert/src/Assert.php' | sha256sum --check

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-xml php8.5-xdebug \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
RUN { php --version | head -1; php -r 'echo "libxml ", LIBXML_DOTTED_VERSION, PHP_EOL;'; } > /work/toolchain.txt
COPY autoload.php harness.php summary.php fuzz-target.php run-control.php target.json /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/run-control.php"]
