FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev llvm ninja-build python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# DuckDB v2.0.0 release-tag archive (MIT).
RUN curl --fail --location --retry 3 https://codeload.github.com/duckdb/duckdb/tar.gz/refs/tags/v2.0.0 --output /work/duckdb.tar.gz \
    && echo '7e89053255046bfb26afbd7f524a2fb84df7dbef496aa911ea35e4a1182fdc00  /work/duckdb.tar.gz' | sha256sum --check \
    && tar -xf /work/duckdb.tar.gz -C /work && mv /work/duckdb-2.0.0 /work/duckdb-src \
    && grep -q 'Permission is hereby granted, free of charge' /work/duckdb-src/LICENSE
COPY harness.cpp parser-probe.cpp build.sh afl-allowlist.txt /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/parser-probe /work/afl-instrumented-objects.txt /work/
COPY --from=build /work/build-cov/src/parser /work/build-cov/src/parser
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh summarize.py manifest.json /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
