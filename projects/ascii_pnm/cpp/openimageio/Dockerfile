FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev libfmt-dev libimath-dev libjpeg-dev libopenexr-dev libopencolorio-dev libtiff-dev llvm ninja-build pkg-config python3 robin-map-dev zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /usr/lib/aarch64-linux-gnu/cmake \
 && ln -s /usr/share/cmake /usr/lib/aarch64-linux-gnu/cmake/OpenColorIO
WORKDIR /work
RUN curl --fail --location --retry 3 --silent --show-error https://github.com/AcademySoftwareFoundation/OpenImageIO/archive/refs/tags/v3.2.2.0.tar.gz -o /work/source.tar.gz \
 && echo 'fa94876cfbd4c817deaba81ced8bad4af2956689faf4085f277b20197cd70b4e  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libfmt10 libimath-3-1-29t64 libjpeg8 libopenexr-3-1-30 libopencolorio2.5 libtiff6 llvm python3 zlib1g libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/install /work/install
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/install/lib
ENTRYPOINT ["/work/run-control.sh"]
