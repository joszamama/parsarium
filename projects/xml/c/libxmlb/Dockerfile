FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends binutils ca-certificates clang curl libclang-rt-21-dev libffi-dev libpcre2-dev llvm meson ninja-build pkg-config python3 python3-packaging xz-utils zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/hughsie/libxmlb/releases/download/0.3.30/libxmlb-0.3.30.tar.xz -o /work/source.tar.xz \
 && echo '2cb894b873aac5fc9e9b6228d4e795f7236d16e429ed2de8f95179a131be3a68  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1 \
 && curl --fail --location --retry 3 https://download.gnome.org/sources/glib/2.88/glib-2.88.4.tar.xz -o /work/glib.tar.xz \
 && echo '25fd169f3b2f91fe2391ad297883ce0fcf30c69fc789ffd1c9672d1332b1c5a8  /work/glib.tar.xz' | sha256sum --check \
 && mkdir /work/glib && tar -xJf /work/glib.tar.xz -C /work/glib --strip-components=1
COPY harness.c harness.h replay.c build.sh afl-allowlist.txt /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libatomic1 libffi8 libpcre2-8-0 llvm python3 libstdc++6 zlib1g \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/glib/glib/gmarkup.c /work/glib/glib/gmarkup.c
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
