FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev libopenal-dev llvm make python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://github.com/liballeg/allegro5/releases/download/5.2.11.3/allegro-5.2.11.3.tar.gz' -o /work/source.tar.gz \
 && echo 'aba4679a5b1f2bf62482eba6e8814a94de7ffc86de5f8587ba199fcc61b4a04f  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1
COPY build-source.sh /work/build-source.sh
RUN chmod +x /work/build-source.sh && /work/build-source.sh
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libopenal1 llvm python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/install/lib /work/install/lib
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/install/lib ALSOFT_DRIVERS=null
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
