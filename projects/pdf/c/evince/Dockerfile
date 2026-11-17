FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl desktop-file-utils gettext libclang-rt-21-dev libcairo2-dev \
    libfreetype-dev libglib2.0-dev libgtk-3-dev libhandy-1-dev libxml2-dev \
    llvm meson ninja-build pkg-config python3 xz-utils zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://poppler.freedesktop.org/poppler-26.11.0.tar.xz -o /work/poppler.tar.xz \
    && echo '41c32680160addf5a8dd7a830e4869c01e9f6bee1abb91e44fabd1ba9d7828fb  /work/poppler.tar.xz' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/poppler.tar.xz -C /work/source --strip-components=1 \
    && curl --fail --location --retry 3 https://download.gnome.org/sources/evince/48/evince-48.4.tar.xz -o /work/evince.tar.xz \
    && echo 'f296c5c662886635d4cd597e8ac0afcde7982be4486533c2b7f095b268be8668  /work/evince.tar.xz' | sha256sum --check \
    && mkdir /work/evince-source && tar -xJf /work/evince.tar.xz -C /work/evince-source --strip-components=1 \
    && echo '346263fc156a1554ea85d91385f7bdb751d7fb63cf22af758e5a8e7318b239e1  /work/evince-source/backend/pdf/ev-poppler.c' | sha256sum --check \
    && echo '7ae4104baf6f522ff3570747e4c1108677ed7628ab95218981b50e73b2c8a920  /work/evince-source/libdocument/ev-document-factory.c' | sha256sum --check
COPY poppler-source-lock.json check-poppler-source.py /work/
RUN python3 -I /work/check-poppler-source.py /work/poppler-source-lock.json /work/source
COPY harness.h harness.c replay.c build.sh afl-allowlist.txt /work/
ENV AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt PKG_CONFIG_PATH=/work/install/lib/pkgconfig
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; pkg-config --modversion poppler-glib evince-document-3.0; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libcairo2 libfreetype6 libgdk-pixbuf-2.0-0 libglib2.0-0t64 \
    libgtk-3-0t64 libhandy-1-0 libstdc++6 libxml2-16 llvm python3 \
    shared-mime-info zlib1g \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/install/lib /work/install/lib
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/install/lib EV_BACKENDS_DIR=/work/install/lib/evince/4/backends LLVM_PROFILE_FILE=/dev/null \
    AFL_PRELOAD=/work/install/lib/evince/4/backends/libpdfdocument.so
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
