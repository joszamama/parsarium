FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl gettext intltool libclang-rt-21-dev libglib2.0-dev libsqlite3-dev libxml2-dev llvm make pkg-config python3 xz-utils && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# libgda 5.2.10 GNOME release tarball (the libgda5 Debian source). build.sh regenerates the Lemon
# parsers with the bundled lemon and removes their #line directives so coverage maps to the C files.
RUN curl --fail --location --retry 3 https://download.gnome.org/sources/libgda/5.2/libgda-5.2.10.tar.xz --output /work/libgda.tar.xz \
    && echo '6f6cdf7b8053f553b907e0c88a6064eb48cf2751852eb24323dcf027792334c8  /work/libgda.tar.xz' | sha256sum --check \
    && tar -xf /work/libgda.tar.xz -C /work && mv /work/libgda-5.2.10 /work/libgda-src \
    && grep -q 'GNU LIBRARY GENERAL PUBLIC LICENSE' /work/libgda-src/COPYING.LIB
COPY harness.c parser-probe.c build.sh afl-allowlist.txt /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends libglib2.0-0t64 libsqlite3-0 libxml2-16 llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/parser-probe /work/afl-instrumented-objects.txt /work/
COPY --from=build /work/build-cov/libgda /work/build-cov/libgda
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh summarize.py manifest.json /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
