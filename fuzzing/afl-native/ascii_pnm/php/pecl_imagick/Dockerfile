# AFL++ feedback is restricted to PECL Imagick C entrypoints; ImageMagick coder source is not instrumented.
FROM --platform=linux/arm64 parsarium/ascii_pnm-php-pecl_imagick:local
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libomp-21-dev make pkg-config autoconf php8.5-dev=8.5.4-0ubuntu1.5 libmagickwand-7.q16-dev=8:7.1.2.18+dfsg1-1 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://pecl.php.net/get/imagick-3.8.1.tgz --output /work/imagick-3.8.1.tgz \
    && echo '3a3587c0a524c17d0dad9673a160b90cd776e836838474e173b549ed864352ee  /work/imagick-3.8.1.tgz' | sha256sum --check \
    && mkdir -p /work/afl-source && tar -xzf /work/imagick-3.8.1.tgz -C /work/afl-source
WORKDIR /work/afl-source/imagick-3.8.1
RUN printf 'src:imagick-3.8.1/imagick_class.c\n' > /work/afl-allowlist.txt \
    && phpize8.5 \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt CC=afl-clang-fast \
       ./configure --with-php-config=/usr/bin/php-config8.5 --with-imagick=/usr \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt make -j4 \
    && mkdir -p /opt/imagick-afl && cp modules/imagick.so /opt/imagick-afl/imagick.so \
    && clang -shared -o /opt/imagick-afl/libaflrt.so /usr/lib/afl/afl-compiler-rt.o
COPY fuzzing/afl-native/ascii_pnm/php/pecl_imagick/fuzzer /work/fuzzer
RUN chmod +x /work/fuzzer
ENTRYPOINT ["/work/fuzzer"]
