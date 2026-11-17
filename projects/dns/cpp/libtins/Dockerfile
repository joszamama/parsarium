FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev llvm ninja-build python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/mfontanini/libtins/archive/refs/tags/v4.6.tar.gz --output /work/libtins.tar.gz \
    && echo '37a9cc407929c56c2081e717347cac455287ba354016bad5bad6243d1f0a4a7a  /work/libtins.tar.gz' | sha256sum --check \
    && tar -xf /work/libtins.tar.gz -C /work && mv /work/libtins-4.6 /work/libtins-src \
    && grep -q 'Redistribution and use in source and binary forms' /work/libtins-src/LICENSE
COPY harness.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/libtins-src /work/libtins-src
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
