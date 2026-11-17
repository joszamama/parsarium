FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://codeload.github.com/marzer/tomlplusplus/tar.gz/refs/tags/v3.4.0 -o /work/source.tar.gz \
    && echo '8517f65938a4faae9ccf8ebb36631a38c1cadfb5efa85d9a72e15b9e97d25155  /work/source.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
    && echo '529bc3900a9571e49db285b0df432397e70b881cc3bf48de6667ae74ff4b06d8  /work/source/LICENSE' | sha256sum --check
COPY harness.cpp typed-tree.h parser-probe.cpp build.sh afl-allowlist.txt /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/parser-probe /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh manifest.json /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
