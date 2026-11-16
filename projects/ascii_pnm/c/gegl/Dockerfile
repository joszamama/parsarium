FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm meson ninja-build pkg-config xz-utils \
    libbabl-dev libglib2.0-dev libjson-glib-dev libjpeg-dev libpng-dev python3 gettext \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://download.gimp.org/pub/gegl/0.4/gegl-0.4.72.tar.xz -o /work/source.tar.xz \
 && echo 'ccbb8cdd1db56ecd4ece5dbabae0118ab2c46b5b3439c94f3cec467798ce956d  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
COPY harness.c harness.h replay.c build.sh run-control.sh /work/
RUN chmod +x /work/build.sh /work/run-control.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libclang-rt-21-dev libbabl-dev libglib2.0-dev libjson-glib-dev libjpeg-dev libpng-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/gegl-cov /opt/gegl-cov
COPY --from=build /opt/gegl-fuzz /opt/gegl-fuzz
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/source/operations/external/ppm-load.c /work/source/operations/external/ppm-load.c
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENV LD_LIBRARY_PATH=/opt/gegl-fuzz/lib GEGL_PATH=/opt/gegl-fuzz/lib/gegl-0.4 ASAN_OPTIONS=detect_leaks=0
ENTRYPOINT ["/work/run-control.sh"]
