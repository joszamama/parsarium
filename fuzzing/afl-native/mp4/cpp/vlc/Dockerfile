# AFL++ overlay for projects/mp4/cpp/vlc: same pinned VLC 3.0.24 static build as the C path; only the MP4 demuxer plugin is instrumented and the C++17 harness is left uninstrumented
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 ca-certificates clang curl libclang-rt-21-dev llvm make pkg-config python3 xz-utils zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://get.videolan.org/vlc/3.0.24/vlc-3.0.24.tar.xz' -o /work/source.tar.xz \
 && echo 'e7cab503d1d7d5849b89d2cf0e1ee60d0ef6d012407791b644b9cfc0cc225fdf  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
COPY harness.cpp harness.h replay.cpp fuzz.cpp build.sh /work/
RUN chmod +x /work/build.sh && PARSARIUM_BUILD=afl /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | grep 'LLVM version'; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 libstdc++6 python3 zlib1g \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/toolchain.txt /work/afl-allowlist.txt /work/
ENTRYPOINT ["/work/fuzzer"]
