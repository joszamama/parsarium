# AFL++ feedback from SAIL 1.3.1's native PNM codec only.
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 ca-certificates clang cmake curl make \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/HappySeaFox/sail/archive/refs/tags/v1.3.1.tar.gz -o /work/source.tar.gz \
 && echo 'bf2905717c06b4ff4269dec010339a85994be9cc524fa3dcde3734b4df376089  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1
COPY projects/ascii_pnm/c/sail/harness.c projects/ascii_pnm/c/sail/harness.h projects/ascii_pnm/c/sail/replay.c /work/
RUN printf 'src:src/sail-codecs/pnm/pnm.c\n' > /work/afl-allowlist.txt \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt cmake -S /work/source -B /work/build -DCMAKE_C_COMPILER=afl-clang-fast -DCMAKE_BUILD_TYPE=Debug \
    -DBUILD_SHARED_LIBS=OFF -DSAIL_ONLY_CODECS=pnm -DSAIL_BUILD_APPS=OFF -DSAIL_BUILD_BINDINGS=OFF -DSAIL_BUILD_EXAMPLES=OFF \
    -DBUILD_TESTING=OFF -DSAIL_ENABLE_OPENMP=OFF -DSAIL_MANIP_USE_SWSCALE=OFF \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt cmake --build /work/build -j4 \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt afl-clang-fast -O1 -g -I/work/source/src -I/work/build/include \
    /work/harness.c /work/replay.c \
    /work/build/src/sail/libsail.a /work/build/src/sail-manip/libsail-manip.a \
    /work/build/src/sail-codecs-archive/libsail-codecs.a /work/build/src/sail-common/libsail-common.a \
    -o /work/fuzzer
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/fuzzer /work/fuzzer
ENTRYPOINT ["/work/fuzzer"]
