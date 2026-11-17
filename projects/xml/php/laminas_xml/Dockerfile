FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/laminas/laminas-xml/legacy.zip/ca5f2b5abf47c7d955680f47c61b5a1225f61999 --output /work/laminas-xml.zip \
    && echo '315cb8243bde1f2dd22292cfd39aed8334e414688b2ee91053314f44685f62cf  /work/laminas-xml.zip' | sha256sum --check \
    && unzip -q /work/laminas-xml.zip -d /work/x \
    && mkdir -p /work/vendor/laminas && mv /work/x/laminas-* /work/vendor/laminas/laminas-xml \
    && echo '40f4348d58cdb54e442ad698de0a990144f38e166f2f77bfb60f658c9252b9c7  /work/vendor/laminas/laminas-xml/LICENSE.md' | sha256sum --check \
    && echo '861ea721a6cec020fd894c2d167c6c9b7770cd616d812838a414937bdc561eea  /work/vendor/laminas/laminas-xml/composer.json' | sha256sum --check \
    && echo '9a9eeb81c46af2f965add1e8f5c4a570f3692e44b0db911c9538a2143faaad3b  /work/vendor/laminas/laminas-xml/src/Security.php' | sha256sum --check

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
