FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/selmf/unarr/archive/refs/tags/v1.2.0.tar.gz -o /work/source.tar.gz \
    && echo 'eba65db354a887c40b39e9f341553977bebc7a293f96c5e1d888064f8d9dd443  /work/source.tar.gz' | sha256sum --check \
    && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
    && python3 -c 'from pathlib import Path; p=Path("/work/source/CMakeLists.txt");s=p.read_text();old="set_target_properties(unarr PROPERTIES INTERPROCEDURAL_OPTIMIZATION TRUE)";assert s.count(old)==1;s=s.replace(old,old.replace("TRUE","FALSE"));prefix="-ffile-prefix-map=${PROJECT_SOURCE_DIR}=unarr";assert s.count(prefix)==1;p.write_text(s.replace(prefix,""))' \
    && echo '8496e3c0e1e32cb17f92ed4bf92d82da62032245813d1dd397667f96ebd62a9a  /work/source/CMakeLists.txt' | sha256sum --check
COPY harness.c harness.h replay.c build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 zlib1g \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
