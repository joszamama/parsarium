FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
 ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/axiomatic-systems/Bento4/archive/refs/tags/v1.6.0-641.tar.gz -o /work/source.tar.gz \
 && echo 'e6575877708526e399cff752b4ee23cb1e2ac32fb251e2ca0a1e8d691fd172a7  /work/source.tar.gz' | sha256sum --check \
 && tar -xzf /work/source.tar.gz -C /work
COPY source-lock.json check-source.py /work/
RUN python3 -I /work/check-source.py /work/source-lock.json /work/Bento4-1.6.0-641
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | head -1; cmake --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
 libstdc++6 llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
