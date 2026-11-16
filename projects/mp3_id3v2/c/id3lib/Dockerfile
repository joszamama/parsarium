FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm make python3 zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://downloads.sourceforge.net/project/id3lib/id3lib/3.8.3/id3lib-3.8.3.tar.gz' -o /work/source.tar.gz \
 && echo '2749cc3c0cd7280b299518b1ddf5a5bcfe2d1100614519b68702230e26c7d079  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1
COPY build-source.sh /work/build-source.sh
RUN chmod +x /work/build-source.sh && /work/build-source.sh
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libstdc++6 llvm python3 zlib1g \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/install /work/install
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/install/lib
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
