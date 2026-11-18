FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm make patch python3 xz-utils \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://deb.debian.org/debian/pool/main/r/rxp/rxp_1.5.0.orig.tar.gz -o /work/source.tar.gz \
 && echo 'a6deff92086018f2b9b53c2ecc37ead94adaaf1e60c1df82ed447e6e462e6678  /work/source.tar.gz' | sha256sum --check \
 && curl --fail --location --retry 3 https://deb.debian.org/debian/pool/main/r/rxp/rxp_1.5.0-3.1.debian.tar.xz -o /work/debian.tar.xz \
 && echo '1f438b4fc517e7e9160a8e4a1b9db854f2a5fc405e810683677525e1697dbbd3  /work/debian.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
 && tar -xJf /work/debian.tar.xz -C /work
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
