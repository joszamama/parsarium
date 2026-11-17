FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/ithewei/libhv/archive/refs/tags/v1.3.1.tar.gz \
    -o /work/source.tar.gz \
    && echo 'da4757c3520854cf2081f796733f7bc023651d60baab448a06fcf66435a859be  /work/source.tar.gz' | sha256sum --check \
    && tar -xzf /work/source.tar.gz -C /work \
    && printf '%s\n' \
    'e55060d9b984564a91543ef9879bbd1fe2dd102025df98a8e6a36d3e4b58e8e1  /work/libhv-1.3.1/LICENSE' \
    'fb2eb5c5e3b52c94aa6efb92dce420926bcfd12c01b59cfa323088725634d7c0  /work/libhv-1.3.1/hexport.h' \
    'e7f5487fd586bab7bfd9a509ac12c44ede4e3bb74d9441f98f215bfa26dd00ce  /work/libhv-1.3.1/http/http_parser.c' \
    'd372dc514ef0223987159c57944cd6e89569145226fde7f539876bf12c458efe  /work/libhv-1.3.1/http/http_parser.h' \
    'b490a5e994e4d3829fba790a9607950622b1737591a68ec67176537288609784  /work/libhv-1.3.1/http/httpdef.c' \
    '9596f5b783886828d1955d47025fdf7da9dc7f011bcfec076615dd0261c9d3d1  /work/libhv-1.3.1/http/httpdef.h' \
    | sha256sum --check
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/libhv-1.3.1 /work/libhv-1.3.1
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
