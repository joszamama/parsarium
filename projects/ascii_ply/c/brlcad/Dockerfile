FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    bison ca-certificates clang cmake curl flex git libclang-rt-21-dev \
    llvm make ninja-build python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://brlcad.org/download/brlcad-7.46.0.tar.gz \
    --output /work/brlcad-7.46.0.tar.gz \
    && echo '7ac576889e3ea83a96eb1f79685cbb47c1314d5a07b57ff55665b229c2ce996c  /work/brlcad-7.46.0.tar.gz' | sha256sum --check \
    && mkdir /work/source \
    && tar -xf /work/brlcad-7.46.0.tar.gz -C /work/source --strip-components=1 \
    && echo '54baa68bd598d40a0a380b4ef044d26ae64a15f86779b802815f56f941b6f306  /work/source/include/gcv/api.h' | sha256sum --check \
    && echo 'e112dcf3cd7c88970c660cc96e0200cd242b0bf41375e669e3ff877bc81e3cbe  /work/source/src/libgcv/plugins/ply/ply_read.c' | sha256sum --check \
    && echo 'a8ab4576417ac3ff2b1230ab607fcc828e22c99b455a592798a648ef3cef6e22  /work/source/src/libgcv/plugins/ply/rply.c' | sha256sum --check \
    && git init /work/bext \
    && git -C /work/bext remote add origin https://github.com/BRL-CAD/bext.git \
    && git -C /work/bext fetch --depth 1 origin 42d8d7ca57f9d2f61192b41f0b41a731f1ba6c47 \
    && git -C /work/bext -c advice.detachedHead=false checkout FETCH_HEAD \
    && test "$(git -C /work/bext rev-parse HEAD)" = 42d8d7ca57f9d2f61192b41f0b41a731f1ba6c47
RUN cmake -S /work/bext -B /work/build/bext_build \
      -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
      -DBEXT_REPOSITORY_ROOT:STRING=https://github.com/BRL-CAD/ \
      -DGIT_SHALLOW_CLONE=ON -DENABLE_ALL=OFF -DUSE_BRLCAD_EXTRA=OFF \
      -DUSE_GDAL=OFF -DUSE_QT=OFF -DUSE_TCL=OFF -DUSE_APPLESEED=OFF \
      -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=/work/build/bext_output \
    && cmake --build /work/build/bext_build --parallel 2 --config Debug
COPY harness.h harness.c replay.c fuzz.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 libstdc++6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/build/lib /work/lib
COPY --from=build /work/build/libexec/gcv /work/libexec/gcv
COPY --from=build /work/build/share /work/share
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/lib
ENV BRLCAD_ROOT=/work
ENV AFL_PRELOAD=/work/libexec/gcv/libgcv-ply.so
ENTRYPOINT ["/work/run-control.sh"]
