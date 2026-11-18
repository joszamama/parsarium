FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev libglib2.0-dev llvm make patch pkg-config python3 xz-utils \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 "https://deb.debian.org/debian/pool/main/g/gdome2/gdome2_0.8.1+debian.orig.tar.gz" -o /work/source.tar.gz \
 && echo 'f4bb80a2ef8e5fd9397ab8aa36d059d0b32e98c4bcf185c7952a7e3874d1d543  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
 && curl --fail --location --retry 3 "https://deb.debian.org/debian/pool/main/g/gdome2/gdome2_0.8.1+debian-10.debian.tar.xz" -o /work/debian.tar.xz \
 && echo 'c309696eacab8959b677361b0880922c0d9b38b5e4bfd9296ea4030181ad0acb  /work/debian.tar.xz' | sha256sum --check \
 && tar -xJf /work/debian.tar.xz -C /work/source \
 && for p in 04bufptr_ftbfs 05gcc10_ftbfs; do patch -d /work/source -p1 < /work/source/debian/patches/$p.patch; done \
 && curl --fail --location --retry 3 https://download.gnome.org/sources/libxml2/2.15/libxml2-2.15.4.tar.xz -o /work/libxml2.tar.xz \
 && echo '98087fd181d9070724f3fbc65c7377db03038eb92bd882374daff44940138821  /work/libxml2.tar.xz' | sha256sum --check \
 && mkdir /work/libxml2-source && tar -xJf /work/libxml2.tar.xz -C /work/libxml2-source --strip-components=1
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libglib2.0-0t64 llvm python3 libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/libxml2-source /work/libxml2-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
