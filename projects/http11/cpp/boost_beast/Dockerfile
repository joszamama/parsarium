FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://archives.boost.io/release/1.92.0/source/boost_1_92_0.tar.gz \
    -o /work/source.tar.gz \
    && echo 'c4a3b310ddd2472416e091067166b0713be97c63f38c212c484ada022fd296ce  /work/source.tar.gz' | sha256sum --check \
    && tar -xzf /work/source.tar.gz -C /work boost_1_92_0/boost boost_1_92_0/LICENSE_1_0.txt \
    && rm /work/source.tar.gz \
    && printf '%s\n' \
       'c74f69f2b30ebbee261eb82f308bb75905ac8bc2385733bdd711af24802a57c5  /work/boost_1_92_0/boost/beast/http/basic_parser.hpp' \
       'c4382876446bbeeec8bfb003305141bfb9c71f77d00266b2c709a78455c9c6fe  /work/boost_1_92_0/boost/beast/http/impl/basic_parser.ipp' \
       '47733a65047763b50b1be7d76fe99dab7eddc9712ed9a1c4ad9e7f4f4cce6764  /work/boost_1_92_0/boost/beast/http/detail/basic_parser.ipp' \
       | sha256sum --check
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
    && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/boost_1_92_0/boost/beast /work/boost_1_92_0/boost/beast
COPY --from=build /work/boost_1_92_0/LICENSE_1_0.txt /work/boost_1_92_0/LICENSE_1_0.txt
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
