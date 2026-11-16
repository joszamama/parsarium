FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev libflac-dev libogg-dev libvorbis-dev llvm ninja-build pkg-config python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://github.com/SFML/SFML/archive/refs/tags/3.0.2.tar.gz' -o /work/source.tar.gz \
 && echo '0034e05f95509e5d3fb81b1625713e06da7b068f210288ce3fd67106f8f46995  /work/source.tar.gz' | sha256sum --check \
 && mkdir -p /work/source/sfml && tar -xzf /work/source.tar.gz -C /work/source/sfml --strip-components=1
COPY build-source.sh /work/build-source.sh
RUN chmod +x /work/build-source.sh && /work/build-source.sh
RUN curl --fail --location --retry 3 'https://github.com/SFML/CSFML/archive/refs/tags/3.0.0.tar.gz' -o /work/csfml.tar.gz \
 && echo '903cd4a782fb0b233f732dc5b37861b552998e93ae8f268c40bd4ce50b2e88ca  /work/csfml.tar.gz' | sha256sum --check \
 && mkdir -p /work/source/csfml && tar -xzf /work/csfml.tar.gz -C /work/source/csfml --strip-components=1
COPY build-csfml.sh /work/build-csfml.sh
RUN chmod +x /work/build-csfml.sh && /work/build-csfml.sh
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libflac14 libogg0 libvorbis0a libvorbisenc2 libvorbisfile3 libstdc++6 llvm python3 \
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
