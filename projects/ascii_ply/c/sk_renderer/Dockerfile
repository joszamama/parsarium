FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/source \
    && curl --fail --location --retry 3 https://raw.githubusercontent.com/StereoKit/sk_renderer/v2026.11.3/example/tools/micro_ply.h -o /work/source/micro_ply.h \
    && echo '18e5db4993352b2bca7ad871b07ce157083e3c65d28a8f125e248451bdc9f4b1  /work/source/micro_ply.h' | sha256sum --check
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source/micro_ply.h /work/source/micro_ply.h
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
