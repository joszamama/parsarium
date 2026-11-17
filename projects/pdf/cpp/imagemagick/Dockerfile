FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev libpng-dev llvm make pkg-config python3 xz-utils zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 'https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10080/ghostpdl-10.08.0.tar.xz' -o /work/ghostscript.tar.xz \
 && echo '94943e3c4adb7115d132b3c28b913672f2e62e6a9d802f7e754e716b1634174a  /work/ghostscript.tar.xz' | sha256sum --check \
 && mkdir /work/ghostscript && tar -xJf /work/ghostscript.tar.xz -C /work/ghostscript --strip-components=1
RUN curl --fail --location --retry 3 'https://codeload.github.com/ImageMagick/ImageMagick/tar.gz/refs/tags/7.1.2-35' -o /work/source.tar.gz \
 && echo '40b6fefa88fe16ca5a4b3d3db5133eaebfb0157f21f98530bde8aec5dd5b0776  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV LLVM_PROFILE_FILE=/dev/null
RUN apt-get update -qq && apt-get install -y --no-install-recommends libpng16-16t64 libstdc++6 llvm python3 zlib1g \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/ghostscript/sobin/libgs.so* /work/lib/
COPY --from=build /work/install /work/install
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/lib
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
