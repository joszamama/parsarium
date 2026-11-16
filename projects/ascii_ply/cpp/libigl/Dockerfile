FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev libeigen3-dev=3.4.0-5 llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/libigl/libigl/archive/refs/tags/v2.6.4.tar.gz \
    --output /work/libigl-2.6.4.tar.gz \
    && echo '09fa1b9b44e0ecbd8fbaa17ec8d9ac0cb4efcedcb2427970f8a4e90bc96e0970  /work/libigl-2.6.4.tar.gz' | sha256sum --check \
    && mkdir /work/source \
    && tar -xf /work/libigl-2.6.4.tar.gz -C /work/source --strip-components=1 \
    && echo 'a58ab5f189ed6d4e01295dd1cf0a8e7cb8d31be677fa66565e8bb7c7a442d43b  /work/source/include/igl/readPLY.cpp' | sha256sum --check \
    && echo '5830b66ee2fd2ce4fcc77892c0ecc00d5e6189e00793145f7cd0ce990615f2f3  /work/source/include/igl/tinyply.cpp' | sha256sum --check
COPY harness.h harness.cpp replay.cpp fuzz.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; dpkg-query -W -f='${Version}\n' libeigen3-dev; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 libstdc++6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
