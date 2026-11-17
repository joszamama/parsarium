FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/pocoproject/poco/releases/download/poco-1.15.4-release/poco-1.15.4.tar.gz -o /work/source.tar.gz \
    && echo '525591a43d4b5e9472663f8fa5fb9b7bfbd7ec8a0abe130ef7411531a0ea55c5  /work/source.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1
COPY build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    source \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
COPY harness.cpp parser-probe.cpp /work/
RUN /work/build.sh harness
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/parser-probe /work/parser-probe-afl /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
