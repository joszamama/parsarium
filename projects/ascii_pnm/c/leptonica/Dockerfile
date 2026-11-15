FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/DanBloomberg/leptonica/archive/refs/tags/1.87.0.tar.gz \
    --output /work/leptonica-1.87.0.tar.gz \
    && echo 'fa2b40c5caea96d1bb93a97486262aed8731b69ce25a84a6bf5d25323e33f631  /work/leptonica-1.87.0.tar.gz' | sha256sum --check \
    && tar -xf /work/leptonica-1.87.0.tar.gz -C /work
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; cmake --version | head -1; \
         dpkg-query -W -f='${Package}=${Version}\n' clang-21 llvm-21 cmake; } \
       > /work/toolchain.txt

FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/leptonica-1.87.0 /work/leptonica-1.87.0
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
