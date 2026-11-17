FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://gmsh.info/src/gmsh-4.15.2-source.tgz \
    --output /work/gmsh-4.15.2-source.tgz \
    && echo 'be3f66f225d27ba9fa014f07e83169285da8a051b0e8ab7103d88066b39bdd3e  /work/gmsh-4.15.2-source.tgz' | sha256sum --check \
    && mkdir /work/source \
    && tar -xf /work/gmsh-4.15.2-source.tgz -C /work/source --strip-components=1 \
    && echo '05c906d986976e057e0305027212e2d10dd09915298efe5684627bbe4a9d112f  /work/source/api/gmshc.h' | sha256sum --check \
    && echo '677c69774707600bb8868939f05cbb5cba29bec8d3108543e9c7517366dd2d93  /work/source/src/geo/GModelIO_PLY.cpp' | sha256sum --check
COPY harness.h harness.c replay.c fuzz.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm python3 libstdc++6 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/lib /work/lib
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/lib
ENTRYPOINT ["/work/run-control.sh"]
