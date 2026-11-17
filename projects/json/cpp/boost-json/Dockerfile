FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm python3 xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Boost.JSON's own headers go to /work/source; the other Boost headers it includes stay in /work/boost and are not counted.
RUN curl --fail --location --retry 3 https://github.com/boostorg/boost/releases/download/boost-1.92.0/boost-1.92.0-b2-nodocs.tar.xz -o /work/source.tar.xz \
    && echo 'ea7b982002cc9dfbe59b0b217b206f470dc75f3de0bb2973d844118934d82411  /work/source.tar.xz' | sha256sum --check \
    && mkdir /work/boost && tar -xJf /work/source.tar.xz -C /work/boost --strip-components=1 boost-1.92.0/boost boost-1.92.0/LICENSE_1_0.txt \
    && rm /work/source.tar.xz && mkdir -p /work/source/boost \
    && mv /work/boost/boost/json /work/boost/boost/json.hpp /work/source/boost/ && cp /work/boost/LICENSE_1_0.txt /work/source/
COPY harness.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
