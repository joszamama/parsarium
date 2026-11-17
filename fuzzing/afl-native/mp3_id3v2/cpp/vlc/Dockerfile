# AFL++ overlay for projects/mp3_id3v2/cpp/vlc: same pinned VLC 3.0.24 static build and VLC-pinned TagLib 1.13.1 as the base project; only the MP3 and ID3v2 parsers are instrumented and the C++17 harness is left uninstrumented
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 ca-certificates clang cmake curl libclang-rt-21-dev llvm make patch pkg-config python3 xz-utils zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://get.videolan.org/vlc/3.0.24/vlc-3.0.24.tar.xz' -o /work/source.tar.xz \
 && echo 'e7cab503d1d7d5849b89d2cf0e1ee60d0ef6d012407791b644b9cfc0cc225fdf  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
RUN curl --fail --location --retry 3 'https://taglib.org/releases/taglib-1.13.1.tar.gz' -o /work/taglib.tar.gz \
 && echo 'c8da2b10f1bfec2cd7dbfcd33f4a2338db0765d851a50583d410bacf055cfd0b  /work/taglib.tar.gz' | sha256sum --check \
 && grep -qx "$(sha512sum /work/taglib.tar.gz | cut -d' ' -f1)  taglib-1.13.1.tar.gz" /work/source/contrib/src/taglib/SHA512SUMS \
 && mkdir /work/taglib-1.13.1 && tar -xzf /work/taglib.tar.gz -C /work/taglib-1.13.1 --strip-components=1 \
 && patch -d /work/taglib-1.13.1 -p1 < /work/source/contrib/src/taglib/0001-Implement-ID3v2-readStyle-avoid-worst-case.patch \
 && patch -d /work/taglib-1.13.1 -p1 < /work/source/contrib/src/taglib/0001-Fix-crash-with-invalid-WAV-files-1163-1164.patch
COPY harness.cpp harness.h replay.cpp fuzz.cpp build.sh /work/
RUN chmod +x /work/build.sh && PARSARIUM_BUILD=afl /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | grep 'LLVM version'; cmake --version | head -1; \
      echo "taglib $(PKG_CONFIG_PATH=/work/taglib-install/lib/pkgconfig pkg-config --modversion taglib)"; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 libstdc++6 python3 zlib1g \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/toolchain.txt /work/afl-allowlist.txt /work/
ENTRYPOINT ["/work/fuzzer"]
