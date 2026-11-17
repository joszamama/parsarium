FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN mkdir /work/source \
 && curl --fail --location --retry 3 --silent --show-error https://raw.githubusercontent.com/mccode-dev/McCode/v3.10.2/common/lib/share/interoff-lib.c -o /work/source/interoff-lib.c \
 && echo 'd54efcda615337e69f0f32f9d37d207921154526d50f794dbd633eab87e73fd7  /work/source/interoff-lib.c' | sha256sum --check \
 && curl --fail --location --retry 3 --silent --show-error https://raw.githubusercontent.com/mccode-dev/McCode/v3.10.2/common/lib/share/interoff-lib.h -o /work/source/interoff-lib.h \
 && echo '67828df8b163c57cabfaca9b54ddb7cde8c4b1d3360012bd1ea86cc5023fde43  /work/source/interoff-lib.h' | sha256sum --check
COPY build.sh compat.h harness.c harness.h replay.c fuzz.c /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/generated /work/generated
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
