FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
 ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/strukturag/libheif/releases/download/v1.23.7/libheif-1.23.7.tar.gz -o /work/source.tar.gz \
 && echo 'f7483e818503ea6224c8863e4a56ac02c7089021a98472c811c12aa19faf2475  /work/source.tar.gz' | sha256sum --check \
 && tar -xzf /work/source.tar.gz -C /work
COPY source-lock.json check-source.py /work/
RUN python3 -I /work/check-source.py /work/source-lock.json /work/libheif-1.23.7
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; cmake --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
ENV LLVM_PROFILE_FILE=/dev/null
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
 libstdc++6 llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
