FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang curl libclang-rt-21-dev llvm python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/ToruNiina/pnm/archive/refs/tags/v1.0.1.tar.gz -o /work/source.tar.gz \
 && echo '50ec55e28e3223950bf69470cf7d6dcdc4240858595d2bf0418734d6ba0a2fe6  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
 && python3 -c 'from pathlib import Path; p=Path("/work/source/pnm.hpp");s=p.read_text();import re;t,n=re.subn(r"(this->iy_\s*(?:<=|>=|<|>)\s*)rhs\.ny_",r"\1rhs.iy_",s);assert n==8;p.write_text(t)' \
 && echo '69c6384e78a74c457f7be9f6c1b5fba6276ed08e3a5a5bba8b1906a8df1610c5  /work/source/pnm.hpp' | sha256sum --check
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source/pnm.hpp /work/source/pnm.hpp
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
