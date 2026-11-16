FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 ca-certificates make subversion \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN svn export --non-interactive -r 5358 https://svn.code.sf.net/p/netpbm/code/stable /work/source \
 && echo '6137ebc9d3ab5cc1a7b6c24b9b64723a6818bb43d5037d0963114f20a367dea9  /work/source/version.mk' | sha256sum --check \
 && echo 'a7bd4a2ddf0f81fa9a8925b3471e2d9afeedd55887964873cb0a395636c3ec74  /work/source/lib/libppm1.c' | sha256sum --check \
 && echo 'd3e1f9c762b2e2a00ff886c5ca0a23436e7e3b8388c7a2ab3a929ecd3cb3014b  /work/source/lib/libppm2.c' | sha256sum --check
COPY projects/ascii_pnm/c/netpbm/harness.c projects/ascii_pnm/c/netpbm/harness.h projects/ascii_pnm/c/netpbm/replay.c /work/
RUN cp /work/source/config.mk.in /work/source/config.mk \
 && printf 'src:libppm1.c\nsrc:libppm2.c\n' > /work/afl-allowlist.txt \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt make -C /work/source lib/all NETPBMLIBTYPE=unixstatic CC=afl-clang-fast \
    CFLAGS='-O1 -g' CFLAGS_FOR_BUILD='-O1 -g' -j1 \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt afl-clang-fast -O1 -g \
    -I/work/source/lib/importinc -I/work/source/lib/util/importinc \
    /work/harness.c /work/replay.c /work/source/lib/libnetpbm.a -lm -o /work/fuzzer
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/fuzzer /work/fuzzer
ENTRYPOINT ["/work/fuzzer"]
