FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm python3 xz-utils \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/boostorg/gil/archive/refs/tags/boost-1.92.0.tar.gz -o /work/gil.tar.gz \
 && echo '6d20dbc568efeb0336c1cf4e988a50ad028eb0837b6b7dc85356d46a32955f66  /work/gil.tar.gz' | sha256sum --check \
 && curl --fail --location --retry 3 https://github.com/boostorg/boost/releases/download/boost-1.92.0/boost-1.92.0-b2-nodocs.tar.xz -o /work/boost.tar.xz \
 && echo 'ea7b982002cc9dfbe59b0b217b206f470dc75f3de0bb2973d844118934d82411  /work/boost.tar.xz' | sha256sum --check \
 && mkdir -p /work/source/gil /work/source/boost \
 && tar -xzf /work/gil.tar.gz -C /work/source/gil --strip-components=1 \
 && tar -xJf /work/boost.tar.xz -C /work/source/boost --strip-components=1 \
 && echo 'd5395ced0c6c5913b14e6a055282590b3c2845c394f3e53944dd99bda3d53b8f  /work/source/gil/include/boost/gil/extension/io/pnm/detail/read.hpp' | sha256sum --check
COPY harness.cpp harness.h replay.cpp build.sh run-control.sh /work/
RUN chmod +x /work/build.sh /work/run-control.sh && /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/source/gil/include/boost/gil/extension/io/pnm/detail/read.hpp /work/source/gil/include/boost/gil/extension/io/pnm/detail/read.hpp
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
