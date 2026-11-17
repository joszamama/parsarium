FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/sabre-io/xml/legacy.zip/bec83cbe2f4e1e1ca4254ed8d7caa7e32cc74b05 --output /work/xml.zip \
    && echo 'ff780dcb7389d1c8c2974d858140c6bef427b097e84ae1995ead20f1cf5b9fa3  /work/xml.zip' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/sabre-io/uri/legacy.zip/a926c749dddfb289b8a9b5218d16ac06affdc631 --output /work/uri.zip \
    && echo '9adbe8ebafd256c74262e2d38347aa7044eabb0a8954f7ea6ec46d7cfc1b2a5e  /work/uri.zip' | sha256sum --check \
    && unzip -q /work/xml.zip -d /work/x && unzip -q /work/uri.zip -d /work/u \
    && mkdir -p /work/vendor/sabre && mv /work/x/sabre-io-xml-* /work/vendor/sabre/xml && mv /work/u/sabre-io-uri-* /work/vendor/sabre/uri

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
