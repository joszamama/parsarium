FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev libpng-dev libxml2-dev llvm make pkg-config python3 xz-utils zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://downloads.sourceforge.net/project/graphicsmagick/graphicsmagick/1.3.49/GraphicsMagick-1.3.49.tar.xz -o /work/source.tar.xz \
 && echo '7efa070dc31116b4315061b39f84bc7181e8b060bf61214ec9af851131af9c81  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libpng16-16t64 libxml2-dev llvm python3 zlib1g libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/install /work/install
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
