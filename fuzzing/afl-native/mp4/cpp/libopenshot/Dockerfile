FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 ca-certificates clang cmake curl libasound2-dev \
    libclang-rt-21-dev libomp-21-dev llvm make ninja-build pkg-config python3 \
    qt6-base-dev qt6-svg-dev xz-utils zlib1g-dev \
    && rm -rf /var/lib/apt/lists/* \
    && test "$(dpkg-query -W -f='${Version}' qt6-base-dev)" = '6.10.2+dfsg-7' \
    && test "$(dpkg-query -W -f='${source:Upstream-Version}' qt6-svg-dev)" = '6.10.2'
WORKDIR /work
RUN curl --fail --location --retry 3 https://ffmpeg.org/releases/ffmpeg-9.0.2.tar.xz \
      -o /work/ffmpeg.tar.xz \
    && echo '8c3850283eb25fa026482078a04051e0be17347b09ef81a0849bec15a96e002e  /work/ffmpeg.tar.xz' | sha256sum --check \
    && mkdir /work/ffmpeg && tar -xJf /work/ffmpeg.tar.xz -C /work/ffmpeg --strip-components=1 \
    && echo '533674687505d25db7176cf876036f600e6d8cb25079ffa6b28b4a8e8266eae1  /work/ffmpeg/libavformat/mov.c' | sha256sum --check
RUN curl --fail --location --retry 3 \
      https://github.com/OpenShot/libopenshot-audio/archive/refs/tags/v1.0.2.tar.gz \
      -o /work/libopenshot-audio.tar.gz \
    && echo '4ea883b1b0a7d62a2c39e65138997c947996ecd3040a7b439b83f2dbd353d28a  /work/libopenshot-audio.tar.gz' | sha256sum --check \
    && mkdir /work/libopenshot-audio \
    && tar -xzf /work/libopenshot-audio.tar.gz -C /work/libopenshot-audio --strip-components=1 \
    && echo 'd0495053051967ebe76fb1facd287d79d1ed800da1be75cf501a556bc39a0472  /work/libopenshot-audio/COPYING' | sha256sum --check
RUN curl --fail --location --retry 3 \
      https://github.com/OpenShot/libopenshot/archive/refs/tags/v1.1.1.tar.gz \
      -o /work/libopenshot.tar.gz \
    && echo 'c5d650629b4104ec4368a2e3c183482e07de3e342d78d1e26f1cb297f9973439  /work/libopenshot.tar.gz' | sha256sum --check \
    && mkdir /work/libopenshot && tar -xzf /work/libopenshot.tar.gz -C /work/libopenshot --strip-components=1 \
    && cd /work/libopenshot && printf '%s\n' \
    '308cc64fc7524213d238ca7e3d2379512121d560de7d59ca1f270e236b5cd741  src/FFmpegReader.h' \
    '376c207ebe787ca2f2241c3c7d03bdeccb4414c5f502c23b142abedc00b3d83e  src/FFmpegReader.cpp' \
    'ea8af5e789cb2d4e9b10bce3874982ade163b749b6bfbdb32e2df21c4d106de1  COPYING' \
    | sha256sum --check
COPY build-source.sh /work/build-source.sh
ARG PARSARIUM_BUILD=coverage
RUN chmod +x /work/build-source.sh && PARSARIUM_BUILD=$PARSARIUM_BUILD /work/build-source.sh
COPY harness.h harness.cpp replay.cpp build-harness.sh /work/
RUN chmod +x /work/build-harness.sh && PARSARIUM_BUILD=$PARSARIUM_BUILD /work/build-harness.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; \
         PKG_CONFIG_PATH=/work/install/lib/pkgconfig pkg-config --modversion libavformat; \
         dpkg-query -W -f='qt6-base-dev ${Version}\nqt6-svg-dev ${Version}\nlibasound2-dev ${Version}\nlibomp-21-dev ${Version}\n' \
           qt6-base-dev qt6-svg-dev libasound2-dev libomp-21-dev; } > /work/toolchain.txt

FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 libasound2t64 libomp5 libqt6core6t64 libqt6gui6 \
    libqt6svg6 libqt6widgets6 libstdc++6 llvm python3 zlib1g \
    && rm -rf /var/lib/apt/lists/* \
    && test "$(dpkg-query -W -f='${Version}' libqt6core6t64)" = '6.10.2+dfsg-7'
ENV HOME=/tmp XDG_CACHE_HOME=/tmp LD_LIBRARY_PATH=/work/install/lib
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/toolchain.txt /work/
COPY --from=build /work/install /work/install
COPY --from=build /work/libopenshot/src /work/libopenshot/src
COPY --from=build /work/ffmpeg/libavformat /work/ffmpeg/libavformat
RUN ! ldd /work/replay /work/fuzzer /work/install/lib/libopenshot.so | grep 'not found'
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
