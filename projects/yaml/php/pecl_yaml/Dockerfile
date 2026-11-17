# pecl/yaml 2.3.0 (PIE package php-ext on Packagist; the PECL yaml extension) is C code: yaml.c/parse.c/detect.c
# turn libyaml parser events into PHP values. The image builds PHP 8.5.12 (--disable-all) without coverage, then
# libyaml 0.2.5 and the extension with Clang/LLVM source coverage, so llvm-cov reports ext/yaml and libyaml lines.
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    autoconf ca-certificates clang curl libclang-rt-21-dev llvm make pkg-config unzip xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# The Packagist dist of pecl/yaml 2.3.0 is the GitHub archive of its locked commit; its C sources must equal the
# PECL release tarball yaml-2.3.0.tgz.
RUN curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && curl --fail --location --retry 3 https://pyyaml.org/download/libyaml/yaml-0.2.5.tar.gz --output /work/yaml-0.2.5.tar.gz \
    && echo 'c642ae9b75fee120b2d96c712538bd2cf283228d2337df2cf2988e3c02678ef4  /work/yaml-0.2.5.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/php/pecl-file_formats-yaml/legacy.zip/c1f0d8ba5ef3884846261bbdb91c2ab0b07db44c --output /work/parser-source.zip \
    && echo '3ea4d29a1454043d504d8c3dd1497e0da299e4cdb47416cde027acfc8805a04d  /work/parser-source.zip' | sha256sum --check \
    && curl --fail --location --retry 3 https://pecl.php.net/get/yaml-2.3.0.tgz --output /work/yaml-2.3.0.tgz \
    && echo 'bc8404807a3a4dc896b310af21a7f8063aa238424ff77f27eb6ffa88b5874b8a  /work/yaml-2.3.0.tgz' | sha256sum --check \
    && mkdir /work/source /work/pecl && tar -xJf /work/php-8.5.12.tar.xz -C /work/source && tar -xzf /work/yaml-0.2.5.tar.gz -C /work/source \
    && tar -xzf /work/yaml-2.3.0.tgz -C /work/pecl && unzip -q /work/parser-source.zip -d /work/source \
    && mv /work/source/php-pecl-file_formats-yaml-c1f0d8b /work/source/pecl-yaml-2.3.0 \
    && for file in LICENSE config.m4 detect.c emit.c parse.c php_yaml.h php_yaml_int.h yaml.c; do \
        cmp /work/source/pecl-yaml-2.3.0/$file /work/pecl/yaml-2.3.0/$file || exit 1; done \
    && grep -q '#define PHP_YAML_VERSION "2.3.0"' /work/source/pecl-yaml-2.3.0/php_yaml.h \
    && cd /work/source && sha256sum php-8.5.12/LICENSE pecl-yaml-2.3.0/LICENSE yaml-0.2.5/License > /work/licenses.txt \
    && sha256sum pecl-yaml-2.3.0/yaml.c pecl-yaml-2.3.0/parse.c pecl-yaml-2.3.0/detect.c pecl-yaml-2.3.0/php_yaml.h pecl-yaml-2.3.0/php_yaml_int.h > /work/yaml-sources.txt
WORKDIR /work/source/php-8.5.12
RUN CC=clang CXX=clang++ CFLAGS='-O1 -g' ./configure --prefix=/opt/php --enable-cli --disable-all --without-pcre-jit \
    || { tail -40 config.log; exit 1; } \
    && make -j8 && make install
ENV CC=clang CFLAGS='-O0 -g -fprofile-instr-generate -fcoverage-mapping' LDFLAGS='-fprofile-instr-generate'
WORKDIR /work/source/yaml-0.2.5
RUN ./configure --prefix=/opt/libyaml --disable-static && make -j8 && make install
WORKDIR /work/source/pecl-yaml-2.3.0
RUN /opt/php/bin/phpize && ./configure --with-php-config=/opt/php/bin/php-config --with-yaml=/opt/libyaml \
    && make -j8 && make install \
    && printf 'extension=yaml.so\n' > /opt/php/lib/php.ini \
    && LD_LIBRARY_PATH=/opt/libyaml/lib LLVM_PROFILE_FILE=/tmp/build-%m.profraw /opt/php/bin/php -r 'exit(phpversion("yaml") === "2.3.0" ? 0 : 1);'
RUN { LD_LIBRARY_PATH=/opt/libyaml/lib LLVM_PROFILE_FILE=/tmp/build-%m.profraw sh -c \
        '/opt/php/bin/php -v | head -1; /opt/php/bin/php -r "echo \"yaml \", phpversion(\"yaml\"), PHP_EOL;"; /opt/php/bin/php --ri yaml | grep -i "libyaml version"'; \
      clang --version | head -1; } > /work/toolchain.txt && rm -f /tmp/build-*.profraw

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb llvm python3 \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/libyaml/lib
WORKDIR /work
COPY --from=build /opt/libyaml /opt/libyaml
COPY --from=build /opt/php /opt/php
COPY --from=build /work/toolchain.txt /work/licenses.txt /work/yaml-sources.txt /work/
COPY --from=build /work/source/pecl-yaml-2.3.0 /work/source/pecl-yaml-2.3.0
COPY --from=build /work/source/yaml-0.2.5 /work/source/yaml-0.2.5
COPY summary.php harness.php fuzz-target.php run-control.py run-control.sh target.json /work/
ENTRYPOINT ["/bin/sh", "/work/run-control.sh"]
