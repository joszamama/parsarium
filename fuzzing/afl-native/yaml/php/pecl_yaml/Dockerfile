# AFL++ instruments the parse path behind yaml_parse(): pecl/yaml 2.3.0 yaml.c (the yaml_parse API), parse.c
# (libyaml events to PHP values, alias table, tag callbacks) and detect.c (implicit scalar typing), plus the
# pinned libyaml 0.2.5 reader.c, scanner.c and parser.c. emit.c, libyaml's api/loader/emitter/dumper/writer code
# and the whole PHP runtime stay uninstrumented; PHP is still compiled with afl-clang-fast under an allowlist that
# matches no PHP source, so the php binary carries the AFL++ runtime that the instrumented yaml.so and libyaml need.
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 autoconf ca-certificates clang curl llvm make pkg-config unzip xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && curl --fail --location --retry 3 https://pyyaml.org/download/libyaml/yaml-0.2.5.tar.gz --output /work/yaml-0.2.5.tar.gz \
    && echo 'c642ae9b75fee120b2d96c712538bd2cf283228d2337df2cf2988e3c02678ef4  /work/yaml-0.2.5.tar.gz' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/php/pecl-file_formats-yaml/legacy.zip/c1f0d8ba5ef3884846261bbdb91c2ab0b07db44c --output /work/parser-source.zip \
    && echo '3ea4d29a1454043d504d8c3dd1497e0da299e4cdb47416cde027acfc8805a04d  /work/parser-source.zip' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source && tar -xzf /work/yaml-0.2.5.tar.gz -C /work/source \
    && unzip -q /work/parser-source.zip -d /work/source && mv /work/source/php-pecl-file_formats-yaml-c1f0d8b /work/source/pecl-yaml-2.3.0 \
    && cd /work/source && sha256sum php-8.5.12/LICENSE pecl-yaml-2.3.0/LICENSE yaml-0.2.5/License > /work/licenses.txt \
    && sha256sum pecl-yaml-2.3.0/yaml.c pecl-yaml-2.3.0/parse.c pecl-yaml-2.3.0/detect.c pecl-yaml-2.3.0/php_yaml.h pecl-yaml-2.3.0/php_yaml_int.h > /work/yaml-sources.txt
WORKDIR /work/source/php-8.5.12
RUN printf 'src:parsarium-no-php-source.c\n' > /work/afl-allowlist-php.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt CC=afl-clang-fast CXX=afl-clang-fast++ CFLAGS='-O1 -g' \
    ./configure --prefix=/opt/php --enable-cli --disable-all --without-pcre-jit \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-php.txt make -j8 && make install
# Out-of-tree build: libyaml sources compile as ../../src/<file>.c, so each suffix entry names exactly one file.
WORKDIR /work/source/yaml-0.2.5/build
RUN printf 'src:src/reader.c\nsrc:src/scanner.c\nsrc:src/parser.c\n' > /work/afl-allowlist-libyaml.txt
RUN AFL_LLVM_ALLOWLIST=/work/afl-allowlist-libyaml.txt CC=afl-clang-fast CFLAGS='-O1 -g' \
    ../configure --prefix=/opt/libyaml --disable-static \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-libyaml.txt make -j8 && make install
WORKDIR /work/source/pecl-yaml-2.3.0
RUN printf 'src:pecl-yaml-2.3.0/yaml.c\nsrc:pecl-yaml-2.3.0/parse.c\nsrc:pecl-yaml-2.3.0/detect.c\n' > /work/afl-allowlist-yaml.txt
RUN /opt/php/bin/phpize && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-yaml.txt CC=afl-clang-fast CFLAGS='-O1 -g' \
    ./configure --with-php-config=/opt/php/bin/php-config --with-yaml=/opt/libyaml \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist-yaml.txt make -j8 && make install
RUN cd /work/source && for object in $(find php-8.5.12 yaml-0.2.5/build pecl-yaml-2.3.0 -name '*.o' | sort); do \
        if nm "$object" | grep -q __afl_area_ptr; then echo "$object"; fi; \
    done > /work/afl-instrumented-objects.txt && cat /work/afl-instrumented-objects.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH=/opt/libyaml/lib
WORKDIR /work
COPY --from=build /opt/libyaml /opt/libyaml
COPY --from=build /opt/php /opt/php
COPY --from=build /work/afl-allowlist-php.txt /work/afl-allowlist-libyaml.txt /work/afl-allowlist-yaml.txt /work/afl-instrumented-objects.txt /work/licenses.txt /work/yaml-sources.txt /work/
RUN printf 'extension=yaml.so\n' > /opt/php/lib/php.ini
COPY projects/yaml/php/pecl_yaml/fuzz-target.php projects/yaml/php/pecl_yaml/harness.php projects/yaml/php/pecl_yaml/summary.php /work/
ENTRYPOINT ["/opt/php/bin/php", "/work/fuzz-target.php"]
