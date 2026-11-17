FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    appstream blueprint-compiler ca-certificates clang cmake curl desktop-file-utils \
    gettext libclang-rt-21-dev libcairo2-dev libexempi-dev libfreetype-dev \
    libglib2.0-dev libgtk-4-dev libadwaita-1-dev libxml2-dev \
    llvm meson ninja-build pkg-config python3 xz-utils zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://poppler.freedesktop.org/poppler-26.11.0.tar.xz -o /work/poppler.tar.xz \
    && echo '41c32680160addf5a8dd7a830e4869c01e9f6bee1abb91e44fabd1ba9d7828fb  /work/poppler.tar.xz' | sha256sum --check \
    && mkdir /work/poppler-source && tar -xJf /work/poppler.tar.xz -C /work/poppler-source --strip-components=1 \
    && curl --fail --location --retry 3 https://download.gnome.org/sources/papers/51/papers-51.1.tar.xz -o /work/papers.tar.xz \
    && echo 'ac0db229883b3d2aacbbda1700dc12aa69716664df201120926096f066e4796b  /work/papers.tar.xz' | sha256sum --check \
    && mkdir /work/papers-source && tar -xJf /work/papers.tar.xz -C /work/papers-source --strip-components=1 \
    && echo 'd56905a47de86b0d044e9de3350b9be6742b093e5159ff3a1cf5f08aa9dc366b  /work/papers-source/libdocument/pps-document-factory.c' | sha256sum --check \
    && echo '316580edc57d6c77c8e19094b68c57e54a3871409938d0509dfb6270b2d2db95  /work/papers-source/libdocument/backend/pdf/pps-poppler.c' | sha256sum --check \
    && echo 'cc68a805f3cb31e2248903c082dad236a1401913a5d34bd134052458eae3d5bc  /work/papers-source/libdocument/pps-document-factory.h' | sha256sum --check
COPY poppler-source-lock.json check-poppler-source.py /work/
RUN python3 -I /work/check-poppler-source.py /work/poppler-source-lock.json /work/poppler-source
COPY harness.h harness.c replay.c build.sh afl-allowlist.txt /work/
ENV PKG_CONFIG_PATH=/work/install/lib/pkgconfig
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; pkg-config --modversion poppler-glib papers-document-4.0; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libadwaita-1-0 libexempi8 libgtk-4-1 libglib2.0-0t64 libstdc++6 llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/install/lib /work/install/lib
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/install/lib PPS_BACKENDS_DIR=/work/install/lib/papers/6/backends LLVM_PROFILE_FILE=/dev/null
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
