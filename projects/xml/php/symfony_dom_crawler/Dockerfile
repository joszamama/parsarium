FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/symfony/dom-crawler/legacy.zip/aa0674b52e1bd00502756fbaba8c982b446472e6 --output /work/dom-crawler.zip \
    && echo '7c538ae1812c8f479866e3b74431aa23c6ee75e3402334ceb875180e3a82e55b  /work/dom-crawler.zip' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/symfony/polyfill-ctype/legacy.zip/141046a8f9477948ff284fa65be2095baafb94f2 --output /work/polyfill-ctype.zip \
    && echo '922b0c6b24d1bcb6447d051edc1fc4526bcca5f88ddc4a27d885507872ceecc1  /work/polyfill-ctype.zip' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/symfony/polyfill-mbstring/legacy.zip/122889ed24dc000165bcbfd77ec412f15cbdfc6a --output /work/polyfill-mbstring.zip \
    && echo '560bc33ca56b79d9c285d9a2f14058ac489b6e6341df75c4e49cf87434c6e3ce  /work/polyfill-mbstring.zip' | sha256sum --check \
    && unzip -q /work/dom-crawler.zip -d /work/d && unzip -q /work/polyfill-ctype.zip -d /work/c && unzip -q /work/polyfill-mbstring.zip -d /work/m \
    && mkdir -p /work/vendor/symfony && mv /work/d/symfony-dom-crawler-* /work/vendor/symfony/dom-crawler \
    && mv /work/c/symfony-polyfill-ctype-* /work/vendor/symfony/polyfill-ctype && mv /work/m/symfony-polyfill-mbstring-* /work/vendor/symfony/polyfill-mbstring

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
