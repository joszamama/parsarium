FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Every composer.lock package (veewee/xml 4.14.0, archive 8058a5dd351a00ad4a45dbe9f6e546fc4480a878dac64de8923397f836d300ff)
# is fetched at its locked git reference and checked against its archive sha256.
COPY vendor-archives.txt /work/
RUN grep -v '^#' /work/vendor-archives.txt | while read -r digest name version url; do \
        curl --fail --location --retry 3 "$url" --output /work/package.zip \
        && echo "$digest  /work/package.zip" | sha256sum --check \
        && rm -rf /work/unpacked && unzip -q /work/package.zip -d /work/unpacked \
        && mkdir -p "/work/vendor/$(dirname "$name")" && mv /work/unpacked/* "/work/vendor/$name" || exit 1; \
    done \
    && echo '46899d9ccc0222a13f3f28d207abe1a322d1944c0f3f56405d15f2c2a1c92812  /work/vendor/veewee/xml/LICENSE' | sha256sum --check

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    php8.5-cli php8.5-xml php8.5-xdebug \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/vendor /work/vendor
RUN { php --version | head -1; php -r 'echo "libxml ", LIBXML_DOTTED_VERSION, PHP_EOL;'; } > /work/toolchain.txt
COPY composer.lock autoload.php harness.php summary.php fuzz-target.php run-control.php target.json /work/
ENTRYPOINT ["php", "-d", "xdebug.mode=coverage", "/work/run-control.php"]
