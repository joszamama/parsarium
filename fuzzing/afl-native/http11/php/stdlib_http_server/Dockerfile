# AFL++ instruments PHP's pinned standalone HTTP/1.1 request parser C source.
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 ca-certificates clang curl xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://www.php.net/distributions/php-8.5.12.tar.xz --output /work/php-8.5.12.tar.xz \
    && echo '08bc2eba2a588654ade1357174aa646b761556c862dda0678345ee29ed481209  /work/php-8.5.12.tar.xz' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/php-8.5.12.tar.xz -C /work/source
COPY projects/http11/php/stdlib_http_server/http-parser-harness.c /work/harness.c
COPY projects/http11/php/stdlib_http_server/php_config.h /work/include/php_config.h
RUN printf 'src:sapi/cli/php_http_parser.c\n' > /work/afl-allowlist.txt \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt afl-clang-fast -O2 -g \
       -I/work/include -I/work/source/php-8.5.12/sapi/cli \
       /work/source/php-8.5.12/sapi/cli/php_http_parser.c /work/harness.c -o /work/fuzzer

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get download afl++=4.33c-1.1ubuntu1 \
    && echo '3a1e9c3421208d4065310e95dd65a6b3920762c115bef0c60133cd58a707a21a  afl++_4.33c-1.1ubuntu1_arm64.deb' | sha256sum --check \
    && apt-get install -y --no-install-recommends ./afl++_4.33c-1.1ubuntu1_arm64.deb \
    && rm -f afl++_4.33c-1.1ubuntu1_arm64.deb && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/fuzzer /work/fuzzer
ENTRYPOINT ["/work/fuzzer"]
