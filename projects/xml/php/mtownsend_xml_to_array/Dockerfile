FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/mtownsend5512/xml-to-array/legacy.zip/8e4b08ae0f56f1e2a77b4b88a0e17bce0200350e --output /work/xml-to-array.zip \
    && echo '57a261f641eee98d20e27600e4846ebbcb05150277a67aa167f07ab3b3ce7e2c  /work/xml-to-array.zip' | sha256sum --check \
    && unzip -q /work/xml-to-array.zip -d /work/x \
    && mkdir -p /work/vendor/mtownsend && mv /work/x/mtownsend5512-xml-to-array-* /work/vendor/mtownsend/xml-to-array \
    && echo '435e9871353b2cd07083f10183e7c905c9dc0b291cd343327deaae1748302009  /work/vendor/mtownsend/xml-to-array/LICENSE.md' | sha256sum --check \
    && echo '89c5a3462385a2a318f4acd4debdf869f9ccf28571ee2fe5ec57e9e94cb57ac6  /work/vendor/mtownsend/xml-to-array/composer.json' | sha256sum --check \
    && echo '907ea73dab5567632ccab156ba18d1360dfb00ec785c51e8e1225f9d5aee12d7  /work/vendor/mtownsend/xml-to-array/src/XmlToArray.php' | sha256sum --check \
    && echo 'ca436e1b84db10e8e24d73f57ab5e01bdb288c285bafc4120e1c6bb41433317f  /work/vendor/mtownsend/xml-to-array/src/helpers.php' | sha256sum --check

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
