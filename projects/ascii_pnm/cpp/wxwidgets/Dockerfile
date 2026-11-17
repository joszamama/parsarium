FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    bzip2 ca-certificates clang cmake curl libclang-rt-21-dev libgtk-3-dev \
    llvm ninja-build python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/wxWidgets/wxWidgets/releases/download/v3.3.4/wxWidgets-3.3.4.tar.bz2 \
    --output /work/wxWidgets-3.3.4.tar.bz2 \
    && echo '815c16cafa4fcbfcf25c5c0a3418309c62257b8a3b6f91d85a1367a134f98c98  /work/wxWidgets-3.3.4.tar.bz2' | sha256sum --check \
    && mkdir /work/source \
    && tar -xjf /work/wxWidgets-3.3.4.tar.bz2 -C /work/source --strip-components=1 \
    && echo '2279ca2c76226d2c45c6f75b85e11c717adcfb8d66e0156cf9a0855ebc20b50f  /work/source/src/common/imagpnm.cpp' | sha256sum --check
RUN printf 'src:imagpnm.cpp\n' > /work/afl-allowlist.txt
ENV AFL_LLVM_INSTRUMENT=CLASSIC AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
COPY harness.h harness.cpp replay.cpp fuzz.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libgtk-3-0t64 libpcre2-32-0 libstdc++6 libxtst6 llvm python3 xvfb \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay-bin /work/fuzzer-bin /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/source/src/common/imagpnm.cpp /work/source/src/common/imagpnm.cpp
COPY with-display.sh replay.sh fuzzer.sh map-size.sh run-control.sh map-control.ppm /work/
RUN echo 'f1e86f7bc611601fed6f44a263d8c1f026dd1d0fd66a7dbc8530e245f5561bf1  /work/map-control.ppm' | sha256sum --check \
    && chmod +x /work/with-display.sh /work/replay.sh /work/fuzzer.sh /work/map-size.sh /work/run-control.sh \
    && ln -s /work/replay.sh /work/replay \
    && ln -s /work/fuzzer.sh /work/fuzzer
ENV LLVM_PROFILE_FILE=/dev/null
ENTRYPOINT ["/work/run-control.sh"]
