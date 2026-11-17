FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends bison bzip2 ca-certificates clang curl flex libclang-rt-21-dev libavcodec-dev libavfilter-dev libavformat-dev libavutil-dev libglib2.0-dev libswresample-dev llvm meson ninja-build pkg-config python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://gitlab.freedesktop.org/gstreamer/gstreamer/-/archive/1.28.9/gstreamer-1.28.9.tar.bz2' -o /work/source.tar.bz2 \
 && echo '6f4074f5bdd071a074220a3642b5861410aa6929c179d903feff4af82d9a05d7  /work/source.tar.bz2' | sha256sum --check \
 && mkdir /work/source && tar -xjf /work/source.tar.bz2 -C /work/source --strip-components=1
COPY build-source.sh /work/build-source.sh
RUN chmod +x /work/build-source.sh && /work/build-source.sh
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libavcodec62 libavfilter11 libavformat62 libavutil60 libglib2.0-0t64 libswresample6 llvm python3 libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/install /work/install
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/install/lib
ENV GST_PLUGIN_PATH=/work/install/lib/gstreamer-1.0
ENV GST_PLUGIN_SYSTEM_PATH=/work/install/lib/gstreamer-1.0
ENV GST_REGISTRY_FORK=no
ENV GST_REGISTRY=/tmp/parsarium-gst-registry.bin
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
