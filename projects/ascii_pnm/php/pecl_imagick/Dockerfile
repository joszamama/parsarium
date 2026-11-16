FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev libomp-21-dev llvm make pkg-config autoconf \
    php8.5-dev=8.5.4-0ubuntu1.5 php8.5-cli=8.5.4-0ubuntu1.5 libmagickwand-7.q16-dev=8:7.1.2.18+dfsg1-1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://pecl.php.net/get/imagick-3.8.1.tgz --output /work/imagick-3.8.1.tgz \
    && echo '3a3587c0a524c17d0dad9673a160b90cd776e836838474e173b549ed864352ee  /work/imagick-3.8.1.tgz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/imagick-3.8.1.tgz -C /work/source
WORKDIR /work/source/imagick-3.8.1
RUN phpize8.5 \
    && CC=clang CFLAGS='-O0 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
       ./configure --with-php-config=/usr/bin/php-config8.5 --with-imagick=/usr \
    && make -j4 \
    && mkdir -p /opt/imagick && cp modules/imagick.so /opt/imagick/imagick.so
RUN { php -v | head -1; php -d extension=/opt/imagick/imagick.so -r 'echo "Imagick ", phpversion("imagick"), PHP_EOL;'; clang --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb llvm python3 php8.5-cli=8.5.4-0ubuntu1.5 libmagickwand-7.q16-10=8:7.1.2.18+dfsg1-1 libomp5 \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/imagick /opt/imagick
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/source/imagick-3.8.1/imagick_class.c /work/source/imagick-3.8.1/imagick_class.c
COPY harness.php control.php fuzz-target.php run-control.sh run-control.py target.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
