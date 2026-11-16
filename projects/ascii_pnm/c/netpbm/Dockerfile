FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang libclang-rt-21-dev llvm make python3 subversion \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN svn export --non-interactive -r 5358 https://svn.code.sf.net/p/netpbm/code/stable /work/source \
 && echo '6137ebc9d3ab5cc1a7b6c24b9b64723a6818bb43d5037d0963114f20a367dea9  /work/source/version.mk' | sha256sum --check \
 && echo 'a7bd4a2ddf0f81fa9a8925b3471e2d9afeedd55887964873cb0a395636c3ec74  /work/source/lib/libppm1.c' | sha256sum --check \
 && echo 'd3e1f9c762b2e2a00ff886c5ca0a23436e7e3b8388c7a2ab3a929ecd3cb3014b  /work/source/lib/libppm2.c' | sha256sum --check
COPY harness.c harness.h replay.c build.sh run-control.sh /work/
RUN chmod +x /work/build.sh /work/run-control.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY --from=build /work/source/lib/libppm1.c /work/source/lib/libppm1.c
COPY --from=build /work/source/lib/libppm2.c /work/source/lib/libppm2.c
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
