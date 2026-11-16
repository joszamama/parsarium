FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/ddiakopoulos/tinyply/archive/refs/tags/3.0.tar.gz \
    -o /work/source.tar.gz \
    && echo '928f95f36c9dfcadffe6c1c349be8e7382e16c5faab9ae72f2e4f368a11a8bd4  /work/source.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
    && echo '69b5e52bce3cc2985530b775e15292aad0824ea3987cb3d419b09339bc06e9d0  /work/source/source/tinyply.h' | sha256sum --check
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends libstdc++6 llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source/source/tinyply.h /work/source/source/tinyply.h
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
