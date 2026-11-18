FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/Imangazaliev/DiDOM/legacy.zip/50fa6595d14f22c0c984efed5c818485cf548136 --output /work/didom.zip \
    && echo '35124c32ae958be5b73e46c2f8e4cf8fd65e5b64c0e83d7fe72de5eea48cf762  /work/didom.zip' | sha256sum --check \
    && unzip -q /work/didom.zip -d /work/x \
    && mkdir -p /work/vendor/imangazaliev && mv /work/x/Imangazaliev-* /work/vendor/imangazaliev/didom \
    && echo 'deff0cbe9b4905fd71e13219816aa435aa750835de76d0820cf96e9ec89aaef1  /work/vendor/imangazaliev/didom/LICENSE' | sha256sum --check \
    && echo '451f3517c35e767d2ff913e10151ece5f061384bd8def697768a24bcd566310e  /work/vendor/imangazaliev/didom/composer.json' | sha256sum --check \
    && echo 'fffadc6f50b187a210a36fbb29b629a7f4591d41c0719b565f65bb2cf24b8f91  /work/vendor/imangazaliev/didom/src/DiDom/Document.php' | sha256sum --check

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
