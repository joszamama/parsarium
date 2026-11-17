FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev libfreetype-dev llvm pkg-config python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://github.com/juce-framework/JUCE/archive/refs/tags/9.0.5.tar.gz' -o /work/source.tar.gz \
 && echo 'd92207f51ba728d3d195b6d5e93ecd049717a915fc250ff6844c32ea7272315a  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1
COPY source-lock.json check-source.py /work/
RUN python3 -I /work/check-source.py /work/source-lock.json /work/source
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libfreetype6 libstdc++6 llvm python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY one-pixel.svg /work/one-pixel.svg
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
