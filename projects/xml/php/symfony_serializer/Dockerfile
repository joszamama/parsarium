FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/symfony/serializer/legacy.zip/05624c94507c3acf065b6486bb626f0d741af459 --output /work/serializer.zip \
    && echo '146260ba0f9fe210bc69a0a29535578b1c4ac07981b9dc15f1b8fe7bb79728de  /work/serializer.zip' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/symfony/deprecation-contracts/legacy.zip/feb1edf4e546af3b85c5caebe8359a20db230ca3 --output /work/deprecation-contracts.zip \
    && echo '284796ef0bf256f751e424a1f14763bc459cfe9fada8a0eb5eb3d2762587be0e  /work/deprecation-contracts.zip' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/symfony/polyfill-ctype/legacy.zip/141046a8f9477948ff284fa65be2095baafb94f2 --output /work/polyfill-ctype.zip \
    && echo '922b0c6b24d1bcb6447d051edc1fc4526bcca5f88ddc4a27d885507872ceecc1  /work/polyfill-ctype.zip' | sha256sum --check \
    && unzip -q /work/serializer.zip -d /work/s && unzip -q /work/deprecation-contracts.zip -d /work/d && unzip -q /work/polyfill-ctype.zip -d /work/c \
    && mkdir -p /work/vendor/symfony && mv /work/s/symfony-serializer-* /work/vendor/symfony/serializer \
    && mv /work/d/symfony-deprecation-contracts-* /work/vendor/symfony/deprecation-contracts && mv /work/c/symfony-polyfill-ctype-* /work/vendor/symfony/polyfill-ctype \
    && echo '18da7e490d2aa77197a0619b25bcc771a0110132a9d76071665718d3295e73cb  /work/vendor/symfony/serializer/LICENSE' | sha256sum --check

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
