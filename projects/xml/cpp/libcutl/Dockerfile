FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm make python3 xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/libexpat/libexpat/releases/download/R_2_10_0/expat-2.10.0.tar.xz -o /work/expat.tar.xz \
    && echo 'c624ba2998fc65df1163a49641ff3f9ab73138b11641d92c86bee0fb01b1bc7f  /work/expat.tar.xz' | sha256sum --check \
    && mkdir /work/expat-source && tar -xJf /work/expat.tar.xz -C /work/expat-source --strip-components=1 \
    && curl --fail --location --retry 3 'https://deb.debian.org/debian/pool/main/libc/libcutl/libcutl_1.10.0+ds1.orig.tar.xz' -o /work/source.tar.xz \
    && echo '957e9cf366501577bcdbc160a0bcb4eeeea9ba0d21de104340b861622c17218b  /work/source.tar.xz' | sha256sum --check \
    && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/expat-source /work/expat-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
