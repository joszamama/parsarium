FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/technosophos/querypath/legacy.zip/6b8e2395fac61fac25bbe962f94def556cb85f7d --output /work/querypath.zip \
    && echo '10e8e6195661a3e0c1345d2d640e4f9f291fc410b92bd363bf477dbb27c77a60  /work/querypath.zip' | sha256sum --check \
    && unzip -q /work/querypath.zip -d /work/x \
    && mkdir -p /work/vendor/querypath && mv /work/x/technosophos-* /work/vendor/querypath/querypath \
    && echo '987af82a6d3c3c4cc37bfb3dd9d7b1a1ce934ed90da560e1b6335ccb6f3d0e6d  /work/vendor/querypath/querypath/COPYING-MIT.txt' | sha256sum --check \
    && echo 'f7d725c9488dfbad49ebdc93dfc866d285fa90264077a03e6ee38db519cef128  /work/vendor/querypath/querypath/composer.json' | sha256sum --check \
    && echo '5b05d4c1f4d7e7e8d768ae0e0f85b5cfd36ec7c301da9d994da2723164660adc  /work/vendor/querypath/querypath/src/QueryPath.php' | sha256sum --check \
    && echo 'e9bf69b8b7bf3f06c70b1ec25c6349f2c9ca86fe1ba9142a1ce94d5de69695c7  /work/vendor/querypath/querypath/src/QueryPath/DOMQuery.php' | sha256sum --check \
    && echo 'adba710259ff1073c3b9916b55ada2a6ffb26231fde3d3d39141fad8276bc075  /work/vendor/querypath/querypath/src/qp_functions.php' | sha256sum --check

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
