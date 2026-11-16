FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 ca-certificates cmake curl make \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/jasper-software/jasper/releases/download/version-4.2.9/jasper-4.2.9.tar.gz -o /work/source.tar.gz \
 && echo 'f71cf643937a5fcaedcfeb30a22ba406912948ad4413148214df280afc425454  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1
COPY projects/ascii_pnm/c/jasper/harness.c projects/ascii_pnm/c/jasper/harness.h projects/ascii_pnm/c/jasper/replay.c /work/
RUN printf 'src:pnm_dec.c\nsrc:pnm_cod.c\n' > /work/afl-allowlist.txt \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt cmake -S /work/source -B /work/build -DCMAKE_C_COMPILER=afl-clang-fast -DCMAKE_BUILD_TYPE=Debug \
    -DJAS_ENABLE_SHARED=OFF -DJAS_ENABLE_DOC=OFF -DJAS_ENABLE_PROGRAMS=OFF -DJAS_ENABLE_LIBJPEG=OFF -DJAS_ENABLE_LIBHEIF=OFF \
    -DJAS_ENABLE_OPENGL=OFF -DJAS_ENABLE_MULTITHREADING_SUPPORT=OFF -DJAS_INCLUDE_BMP_CODEC=OFF -DJAS_INCLUDE_JP2_CODEC=OFF \
    -DJAS_INCLUDE_JPC_CODEC=OFF -DJAS_INCLUDE_JPG_CODEC=OFF -DJAS_INCLUDE_HEIC_CODEC=OFF -DJAS_INCLUDE_MIF_CODEC=OFF \
    -DJAS_INCLUDE_PGX_CODEC=OFF -DJAS_INCLUDE_RAS_CODEC=OFF -DJAS_INCLUDE_PNM_CODEC=ON -DJAS_ENABLE_PNM_CODEC=ON \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt cmake --build /work/build --target libjasper -j4 \
 && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt afl-clang-fast -O1 -g \
    -I/work/source/src/libjasper/include -I/work/build/src/libjasper/include \
    /work/harness.c /work/replay.c /work/build/src/libjasper/libjasper.a -lm -o /work/fuzzer
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.33c-1.1ubuntu1 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/fuzzer /work/fuzzer
ENTRYPOINT ["/work/fuzzer"]
