FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libcairo2-dev libclang-rt-21-dev libfreetype-dev libglib2.0-dev llvm ninja-build pkg-config python3 xz-utils zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://poppler.freedesktop.org/poppler-26.11.0.tar.xz' -o /work/source.tar.xz \
 && echo '41c32680160addf5a8dd7a830e4869c01e9f6bee1abb91e44fabd1ba9d7828fb  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
COPY source-lock.json check-source.py /work/
RUN python3 -I /work/check-source.py /work/source-lock.json /work/source
COPY build-source.sh /work/build-source.sh
RUN chmod +x /work/build-source.sh && /work/build-source.sh
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; dpkg-query -W -f='${Package} ${Version}\n' libglib2.0-dev libcairo2-dev; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libcairo2 libfreetype6 libglib2.0-0t64 libstdc++6 llvm python3 zlib1g \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/install/lib /work/install/lib
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/install/lib
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
