# AFL++ overlay for projects/mp3/c/mpv: same pinned mpv 0.42.0, FFmpeg 9.0.2 and libplacebo 7.387.0 build as the base project; only FFmpeg's tagged-MP3 parsing sources and mpv's demux_lavf.c are instrumented and the C harness is left uninstrumented
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 ca-certificates clang curl libass-dev libclang-rt-21-dev libfast-float-dev libvulkan-dev llvm make meson ninja-build pkg-config python3 python3-jinja2 xz-utils zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://github.com/mpv-player/mpv/archive/refs/tags/v0.42.0.tar.gz' -o /work/source.tar.gz \
 && echo 'bcfebbfa2b65a6d88dc97ea18117831072373e38b5785a2afb874ed4df5070dd  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
 && echo '11a228fa8e3d7fec72be89d3a606829f071676b041fdce3c12719c056600dce6  /work/source/player/loadfile.c' | sha256sum --check \
 && echo '9fbd9b274b341e272eedce7b6480e809b21d5d5aef080846d3c33d0817200f18  /work/source/demux/demux_lavf.c' | sha256sum --check
# FFmpeg is the release the catalog's Homebrew mpv linked (ffmpeg 9.0.2_1), the
# same libavformat the direct FFmpeg MP3 row pins.
RUN curl --fail --location --retry 3 'https://ffmpeg.org/releases/ffmpeg-9.0.2.tar.xz' -o /work/ffmpeg.tar.xz \
 && echo '8c3850283eb25fa026482078a04051e0be17347b09ef81a0849bec15a96e002e  /work/ffmpeg.tar.xz' | sha256sum --check \
 && mkdir /work/ffmpeg && tar -xJf /work/ffmpeg.tar.xz -C /work/ffmpeg --strip-components=1 \
 && echo '8ace16c6fdd16b296d5a1fbef49e4cf70cc930eb2f040f2a3c8ebe7daedd6205  /work/ffmpeg/libavformat/id3v2.c' | sha256sum --check \
 && echo '0f56e19ca0694798b2dcd40f6a06e412784b2557945958f4c0b2371dcc0718af  /work/ffmpeg/libavformat/mp3dec.c' | sha256sum --check
# mpv 0.42.0 requires libplacebo >= 7.387.0, the release the catalog's Homebrew
# mpv linked. The tag archive has no submodules; jinja2 and fast_float come from
# Ubuntu and the GPU backends that need glad and Vulkan headers are disabled.
RUN curl --fail --location --retry 3 'https://github.com/haasn/libplacebo/archive/refs/tags/v7.387.0.tar.gz' -o /work/libplacebo.tar.gz \
 && echo 'f9e62d3774a9c4cfd198ec3abaa88294aaade2e31c04d5ab02bcf4abc98b1df5  /work/libplacebo.tar.gz' | sha256sum --check \
 && mkdir /work/libplacebo && tar -xzf /work/libplacebo.tar.gz -C /work/libplacebo --strip-components=1
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && PARSARIUM_BUILD=afl /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | grep 'LLVM version'; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV HOME=/tmp XDG_CACHE_HOME=/tmp
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 libass9 libstdc++6 python3 zlib1g \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/toolchain.txt /work/afl-allowlist.txt /work/afl-guarded.txt /work/
ENTRYPOINT ["/work/fuzzer"]
