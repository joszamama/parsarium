# Pinned VLC 3.0.24 source build with VLC's own contrib TagLib pin (1.13.1 plus the two
# contrib patches); the call site is a C++17 translation unit.
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev llvm make patch pkg-config python3 xz-utils zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://get.videolan.org/vlc/3.0.24/vlc-3.0.24.tar.xz' -o /work/source.tar.xz \
 && echo 'e7cab503d1d7d5849b89d2cf0e1ee60d0ef6d012407791b644b9cfc0cc225fdf  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
# TagLib release, URL and SHA-512 come from VLC's contrib/src/taglib (rules.mak, SHA512SUMS);
# the patches are applied in rules.mak order.
RUN curl --fail --location --retry 3 'https://taglib.org/releases/taglib-1.13.1.tar.gz' -o /work/taglib.tar.gz \
 && echo 'c8da2b10f1bfec2cd7dbfcd33f4a2338db0765d851a50583d410bacf055cfd0b  /work/taglib.tar.gz' | sha256sum --check \
 && grep -qx "$(sha512sum /work/taglib.tar.gz | cut -d' ' -f1)  taglib-1.13.1.tar.gz" /work/source/contrib/src/taglib/SHA512SUMS \
 && mkdir /work/taglib-1.13.1 && tar -xzf /work/taglib.tar.gz -C /work/taglib-1.13.1 --strip-components=1 \
 && patch -d /work/taglib-1.13.1 -p1 < /work/source/contrib/src/taglib/0001-Implement-ID3v2-readStyle-avoid-worst-case.patch \
 && patch -d /work/taglib-1.13.1 -p1 < /work/source/contrib/src/taglib/0001-Fix-crash-with-invalid-WAV-files-1163-1164.patch
COPY harness.cpp harness.h replay.cpp fuzz.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | grep 'LLVM version'; cmake --version | head -1; \
      echo "taglib $(PKG_CONFIG_PATH=/work/taglib-install/lib/pkgconfig pkg-config --modversion taglib)"; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV LLVM_PROFILE_FILE=/dev/null
RUN apt-get update -qq && apt-get install -y --no-install-recommends libstdc++6 llvm python3 zlib1g \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh valid-v24.mp3 /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
