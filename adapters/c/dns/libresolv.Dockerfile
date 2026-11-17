FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends clang libc6-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY libresolv.c /work/libresolv.c
RUN clang -O1 -g -Wall -o /work/libresolv /work/libresolv.c -lresolv \
    && { ldd --version | head -1; dpkg-query -W -f='libc6-dev ${Version}\n' libc6-dev; clang --version | head -1; } > /work/runtime.txt
ENTRYPOINT ["/work/libresolv"]
