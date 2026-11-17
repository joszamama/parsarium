FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 ca-certificates clang cmake curl git \
    libclang-rt-21-dev libegl1-mesa-dev libgbm-dev libx11-dev libxfixes-dev \
    libfontconfig1-dev libxrandr-dev libxinerama-dev libxcursor-dev \
    llvm ninja-build python3 unzip zip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 -H 'User-Agent: Parsarium PLY verifier' \
    https://api.github.com/repos/StereoKit/StereoKit/tarball/refs/tags/v0.3.11 \
    --output /work/source.tar.gz \
    && echo '2dfcd144df326733a6d75e171414a6d737b79a538de9edf1e8c705ee9274ec07  /work/source.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
    && echo '81d4a0e03ea8ff044023c545a1b5511d15cad90bd837aba253c633e8c39fbf7e  /work/source/StereoKitC/stereokit.h' | sha256sum --check \
    && echo '5695a9daeb6d225a0dd37b73e34aacaf056ca0d8b5056b59feca6a948d12fa98  /work/source/StereoKitC/asset_types/model_ply.cpp' | sha256sum --check \
    && echo '95d37d8f983c1689689427f6905f9429a3e87476735e53d908411794f0852685  /work/source/StereoKitC/libraries/micro_ply.h' | sha256sum --check
COPY build.sh /work/
ARG PARSARIUM_BUILD=coverage
RUN chmod +x /work/build.sh && PARSARIUM_BUILD=$PARSARIUM_BUILD /work/build.sh source
COPY harness.h harness.c replay.c /work/
RUN PARSARIUM_BUILD=$PARSARIUM_BUILD /work/build.sh harness \
    && { clang --version | head -1; llvm-cov --version | head -1; cmake --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 libegl1 libgbm1 libx11-6 libxfixes3 libfontconfig1 \
    libxrandr2 libxinerama1 libxcursor1 libgl1-mesa-dri libstdc++6 llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV LD_LIBRARY_PATH=/work/lib HOME=/tmp XDG_CACHE_HOME=/tmp
COPY --from=build /work/replay /work/toolchain.txt /work/
COPY --from=build /work/fuzzer /work/fuzzer-bin
COPY --from=build /work/lib /work/lib
COPY --from=build /work/source/StereoKitC/libraries/micro_ply.h /work/source/StereoKitC/libraries/micro_ply.h
COPY --from=build /work/source/StereoKitC/asset_types/model_ply.cpp /work/source/StereoKitC/asset_types/model_ply.cpp
COPY run-control.sh /work/run-control.sh
COPY fuzzer.sh /work/fuzzer
RUN chmod +x /work/run-control.sh /work/fuzzer
ENTRYPOINT ["/work/run-control.sh"]
