FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 ca-certificates clang curl meson ninja-build pkg-config xz-utils \
    libbabl-dev libglib2.0-dev libjson-glib-dev libjpeg-dev libpng-dev python3 gettext \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://download.gimp.org/pub/gegl/0.4/gegl-0.4.72.tar.xz -o /work/source.tar.xz \
 && echo 'ccbb8cdd1db56ecd4ece5dbabae0118ab2c46b5b3439c94f3cec467798ce956d  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
COPY projects/ascii_pnm/c/gegl/harness.c projects/ascii_pnm/c/gegl/harness.h projects/ascii_pnm/c/gegl/replay.c /work/
RUN printf 'src:ppm-load.c\n' > /work/afl-allowlist.txt \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt CC=afl-clang-fast CFLAGS='-O1 -g' \
    meson setup /work/build /work/source --prefix=/opt/gegl-afl --libdir=lib --buildtype=debug \
      --auto-features=disabled -Ddocs=false -Dintrospection=false -Dvapigen=disabled -Dgtk-doc=false -Dgi-docgen=disabled -Doperation-test=false \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt meson compile -C /work/build -j4 \
 && meson install -C /work/build --no-rebuild \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt afl-clang-fast -O1 -g \
    $(PKG_CONFIG_PATH=/opt/gegl-afl/lib/pkgconfig pkg-config --cflags gegl-0.4) \
    /work/harness.c /work/replay.c \
    $(PKG_CONFIG_PATH=/opt/gegl-afl/lib/pkgconfig pkg-config --libs gegl-0.4) \
    -Wl,-rpath,/opt/gegl-afl/lib -o /work/fuzzer
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 libbabl-dev libglib2.0-dev libjson-glib-dev libjpeg-dev libpng-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/gegl-afl /opt/gegl-afl
COPY --from=build /work/fuzzer /work/fuzzer
ENV LD_LIBRARY_PATH=/opt/gegl-afl/lib GEGL_PATH=/opt/gegl-afl/lib/gegl-0.4
ENTRYPOINT ["/work/fuzzer"]
