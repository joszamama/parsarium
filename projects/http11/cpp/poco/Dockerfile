FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://github.com/pocoproject/poco/archive/refs/tags/poco-1.15.4-release.tar.gz \
    --output /work/source.tar.gz \
    && echo '4635007f593646b3db8754bbb31ded34cd533487519d4d4a45c788dbff3fe07f  /work/source.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xf /work/source.tar.gz -C /work/source --strip-components=1 \
    && echo '02ebe8fd7a3cecb12afcb2390301b35987b7814e1472f7a7564466e00edde770  /work/source/Net/src/HTTPRequest.cpp' | sha256sum --check \
    && echo 'ac904026f5f13c302588c9a640fa3381d94a7de98510ca16917cde052025cf82  /work/source/Net/src/HTTPMessage.cpp' | sha256sum --check
COPY harness.h harness.cpp replay.cpp fuzz.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 libstdc++6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
