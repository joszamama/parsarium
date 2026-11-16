FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev libgd-dev libpng-dev libxml2-dev llvm make pkg-config xz-utils zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source
RUN curl --fail --location --retry 3 https://libzip.org/download/libzip-1.12.1.tar.xz --output /work/libzip-1.12.1.tar.xz \
    && echo 'c40062022a1963c80573d48f6070792297cecd7c6bffe3aefcac0d8b9bee8913  /work/libzip-1.12.1.tar.xz' | sha256sum --check \
    && tar -xJf /work/libzip-1.12.1.tar.xz -C /work/source
RUN CC=clang CFLAGS='-O0 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate -Wl,-rpath,/opt/libzip/lib' \
    cmake -S /work/source/libzip-1.12.1 -B /work/libzip-build -DCMAKE_INSTALL_PREFIX=/opt/libzip -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_BUILD_TYPE=Debug \
    -DBUILD_TOOLS=OFF -DBUILD_REGRESS=OFF -DBUILD_OSSFUZZ=OFF -DBUILD_EXAMPLES=OFF -DBUILD_DOC=OFF \
    -DENABLE_COMMONCRYPTO=OFF -DENABLE_GNUTLS=OFF -DENABLE_OPENSSL=OFF -DENABLE_BZIP2=OFF -DENABLE_LZMA=OFF -DENABLE_ZSTD=OFF \
    && cmake --build /work/libzip-build --parallel 4 && cmake --install /work/libzip-build
ENV PKG_CONFIG_PATH=/opt/libzip/lib/pkgconfig LD_LIBRARY_PATH=/opt/libzip/lib
WORKDIR /work/source/php-8.5.12
RUN CC=clang CXX=clang++ CFLAGS='-O0 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate -Wl,-rpath,/opt/libzip/lib' \
    ./configure --prefix=/opt/php --enable-cli --disable-all --enable-gd --with-external-gd --with-zip --enable-phar --with-libxml --with-zlib || { grep -n -A25 'checking whether the C compiler works' config.log; exit 1; } \
    && make -j4 && make install
RUN { /opt/php/bin/php -v | head -1; /opt/php/bin/php -r 'echo "GD ", GD_VERSION, PHP_EOL; echo "ZIP ", phpversion("zip"), " libzip ", ZipArchive::LIBZIP_VERSION, PHP_EOL;'; clang --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb llvm python3 libgd3 libxml2-16 libpng16-16t64 zlib1g \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV LD_LIBRARY_PATH=/opt/libzip/lib
COPY --from=build /opt/libzip /opt/libzip
COPY --from=build /opt/php /opt/php
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/source/libzip-1.12.1/lib/zip_open.c /work/source/libzip-1.12.1/lib/zip_open.c
COPY fuzz-target.php harness.php run-control.py run-control.sh target.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
