FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/ton/PLYwoot/archive/refs/tags/v0.3.0.tar.gz \
    -o /work/source.tar.gz \
    && echo '18d2606eafb8bfc700d1eb57d665f335e4601877a11132a7873d0491ae496701  /work/source.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
    && echo '91a20485e3e5e8d991d3a884d63850abd8fdb460c6fdc927464e8692ea379d64  /work/source/include/plywoot/plywoot.hpp' | sha256sum --check
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends libstdc++6 llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source/include /work/source/include
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
