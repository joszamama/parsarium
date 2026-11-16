FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://acme.com/software/libpnmrw/libpnmrw_14Aug2014.tar.gz -o /work/source.tar.gz \
 && echo 'c4a18cc85066bcd14835c4dce09c0541b3940a1033e89346373d235a6b5a303f  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
 && python3 -c 'from pathlib import Path; p=Path("/work/source/libpnmrw.c");s=p.read_text();assert s.count("e = sys_errlist[errno];")==1;p.write_text(s.replace("e = sys_errlist[errno];","e = strerror(errno);"))' \
 && echo '82fed46225e02b8d700244d89010fcf9680ec52bf14cdcb3c15dd83b3439e8aa  /work/source/libpnmrw.c' | sha256sum --check
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
