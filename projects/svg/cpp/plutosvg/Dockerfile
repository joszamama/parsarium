FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/sammycage/plutosvg/archive/refs/tags/v0.0.8.tar.gz \
    -o /work/plutosvg.tar.gz \
    && echo '49d5cfe772d3aa10cd4879f2f6e189f5083c08e4c8ea01bf3d5b87c97dfca7d2  /work/plutosvg.tar.gz' | sha256sum --check \
    && tar -xzf /work/plutosvg.tar.gz -C /work \
    && curl --fail --location --retry 3 \
    https://github.com/sammycage/plutovg/archive/refs/tags/v1.3.3.tar.gz \
    -o /work/plutovg.tar.gz \
    && echo '2b0d17a6e016f47b86f9c00e2cb82600041b1ea1f7d2a00c2d46ae542cbfed3c  /work/plutovg.tar.gz' | sha256sum --check \
    && tar -xzf /work/plutovg.tar.gz -C /work/plutosvg-0.0.8/plutovg --strip-components=1
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; cmake --version | head -1; } \
       > /work/toolchain.txt

FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libstdc++6 llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/plutosvg-0.0.8/source /work/plutosvg-0.0.8/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
