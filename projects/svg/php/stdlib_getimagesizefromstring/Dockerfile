FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev libgd-dev libpng-dev libxml2-dev libzip-dev llvm make pkg-config xz-utils zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source
WORKDIR /work/source/php-8.5.12
RUN CC=clang CXX=clang++ CFLAGS='-O0 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate' \
    ./configure --prefix=/opt/php --enable-cli --disable-all --enable-gd --with-external-gd --with-zip --enable-phar --with-libxml --with-zlib || { grep -n -A25 'checking whether the C compiler works' config.log; exit 1; } \
    && make -j4 && make install
RUN { /opt/php/bin/php -v | head -1; /opt/php/bin/php -r 'echo "GD ", GD_VERSION, PHP_EOL;'; clang --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb llvm python3 libgd3 libxml2-16 libpng16-16t64 libzip5 zlib1g \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/php /opt/php
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/source/php-8.5.12/ext/standard/image.c /work/source/php-8.5.12/ext/standard/image.c
COPY fuzz-target.php harness.php run-control.py run-control.sh target.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
