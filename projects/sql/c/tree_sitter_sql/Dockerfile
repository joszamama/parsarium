FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# tree-sitter-sql 0.3.11 release archive (generated src/parser.c and src/scanner.c are byte-identical
# to Debian source package tree-sitter-sql 0.3.11-1) and the tree-sitter 0.26.11 runtime (Debian sid version).
RUN curl --fail --location --retry 3 https://github.com/DerekStride/tree-sitter-sql/releases/download/v0.3.11/tree-sitter-sql-v0.3.11.tar.gz --output /work/tree-sitter-sql.tar.gz \
    && echo 'a97a324eae9c81ed68f6e162b9b33f8911fc6442caa2950e57c498e2460d1387  /work/tree-sitter-sql.tar.gz' | sha256sum --check \
    && mkdir -p /work/src/tree-sitter-sql && tar -xzf /work/tree-sitter-sql.tar.gz -C /work/src/tree-sitter-sql \
    && echo 'add99a0bddfd4d210fa60df11046a19eb0a4d3ebf5bcaa065c674b0c9220ef6e  /work/src/tree-sitter-sql/src/parser.c' | sha256sum --check \
    && echo 'de17b5cffc3c86f56cf6630abb969330c3c839a81ece0b901bdac0ecee93c403  /work/src/tree-sitter-sql/src/scanner.c' | sha256sum --check \
    && echo '3b3e4e4252d5d7d1c18e1257005f23242bf0580ad619204fd093c99b8c56748d  /work/src/tree-sitter-sql/LICENSE' | sha256sum --check \
    && curl --fail --location --retry 3 https://codeload.github.com/tree-sitter/tree-sitter/tar.gz/refs/tags/v0.26.11 --output /work/tree-sitter.tar.gz \
    && echo '1bab01ed21464f3272665b9c60e39ee79f68da1333e80b23f2c9356569d06971  /work/tree-sitter.tar.gz' | sha256sum --check \
    && tar -xzf /work/tree-sitter.tar.gz -C /work/src && mv /work/src/tree-sitter-0.26.11 /work/src/tree-sitter \
    && grep -q 'The MIT License (MIT)' /work/src/tree-sitter/LICENSE
COPY harness.c parser-probe.c build.sh afl-allowlist.txt /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/parser-probe /work/afl-instrumented-objects.txt /work/
COPY --from=build /work/src/tree-sitter-sql/src /work/src/tree-sitter-sql/src
COPY --from=build /work/src/tree-sitter/lib /work/src/tree-sitter/lib
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh summarize.py manifest.json /work/
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
