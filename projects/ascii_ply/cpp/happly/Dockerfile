FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/nmwsharp/happly/archive/refs/tags/v1.1.0.tar.gz \
    -o /work/source.tar.gz \
    && echo '424987cdc6d24be4674c09efeed455a91a377d88400a65e5d4e68c368f4c49b9  /work/source.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
    && echo '05a2bc71e9f3a48b2b996d06c5516254132d0f26f52b3fd845aff2492bf51f82  /work/source/happly.h' | sha256sum --check
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends libstdc++6 llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source/happly.h /work/source/happly.h
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
