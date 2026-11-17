FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 ca-certificates clang cmake curl libclang-rt-21-dev \
    llvm make ninja-build pkg-config python3 xz-utils zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://ffmpeg.org/releases/ffmpeg-9.0.2.tar.xz \
      -o /work/ffmpeg.tar.xz \
    && echo '8c3850283eb25fa026482078a04051e0be17347b09ef81a0849bec15a96e002e  /work/ffmpeg.tar.xz' | sha256sum --check \
    && mkdir /work/ffmpeg && tar -xJf /work/ffmpeg.tar.xz -C /work/ffmpeg --strip-components=1 \
    && echo '533674687505d25db7176cf876036f600e6d8cb25079ffa6b28b4a8e8266eae1  /work/ffmpeg/libavformat/mov.c' | sha256sum --check
RUN curl --fail --location --retry 3 \
      https://github.com/mltframework/mlt/releases/download/v7.42.0/mlt-7.42.0.tar.gz \
      -o /work/mlt.tar.gz \
    && echo '8800e343f43aaa885bd5d9d23553030fa220aa3e2f0c94d9fd6a936d41638cdd  /work/mlt.tar.gz' | sha256sum --check \
    && mkdir /work/mlt && tar -xzf /work/mlt.tar.gz -C /work/mlt --strip-components=1 \
    && echo '806971be6c0ef60c08917ae11d138023cc27967b238fa937b48567ada42daa7b  /work/mlt/src/framework/mlt_factory.h' | sha256sum --check \
    && echo '87ade181fa43b953fbb30156adafe476e5ac86a14dee0531d059d0b93804875d  /work/mlt/src/modules/avformat/producer_avformat.c' | sha256sum --check
COPY build-source.sh /work/build-source.sh
ARG PARSARIUM_BUILD=coverage
RUN chmod +x /work/build-source.sh && PARSARIUM_BUILD=$PARSARIUM_BUILD /work/build-source.sh
COPY harness.h harness.c replay.c build-harness.sh /work/
RUN chmod +x /work/build-harness.sh && PARSARIUM_BUILD=$PARSARIUM_BUILD /work/build-harness.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; PKG_CONFIG_PATH=/work/install/lib/pkgconfig pkg-config --modversion libavformat; } > /work/toolchain.txt

FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 llvm python3 libstdc++6 zlib1g \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
ENV LD_LIBRARY_PATH=/work/install/lib MLT_REPOSITORY=/work/install/lib/mlt-7 MLT_DATA=/work/install/share/mlt-7
COPY --from=build /work/replay /work/fuzzer /work/toolchain.txt /work/
COPY --from=build /work/install /work/install
COPY --from=build /work/mlt/src/modules/avformat/producer_avformat.c /work/mlt/src/modules/avformat/producer_avformat.c
COPY --from=build /work/ffmpeg/libavformat/mov.c /work/ffmpeg/libavformat/mov.c
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
