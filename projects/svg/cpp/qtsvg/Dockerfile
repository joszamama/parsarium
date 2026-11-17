FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev llvm ninja-build pkg-config python3 libfontconfig1-dev libfreetype-dev libpng-dev zlib1g-dev libpcre2-dev xz-utils \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 --silent --show-error https://ftp.fau.de/qtproject/archive/qt/6.12/6.12.0/submodules/qtbase-everywhere-src-6.12.0.tar.xz -o /work/qtbase.tar.xz \
 && echo 'a951bd163c7b80fc6b8c88d7668fb56abf91c152373e13c10666763238131307  /work/qtbase.tar.xz' | sha256sum --check \
 && mkdir /work/qtbase && tar -xJf /work/qtbase.tar.xz -C /work/qtbase --strip-components=1
COPY build-qtbase.sh /work/
RUN chmod +x /work/build-qtbase.sh && /work/build-qtbase.sh
RUN curl --fail --location --retry 3 --silent --show-error https://ftp.fau.de/qtproject/archive/qt/6.12/6.12.0/submodules/qtsvg-everywhere-src-6.12.0.tar.xz -o /work/source.tar.xz \
 && echo 'e4ab39534ec97987b1b9b60ef7f4d3253d5912a69f8c713a01753174a4029331  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | head -1; /work/qt/bin/qtpaths --qt-version || true; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libfontconfig1 libfreetype6 libpng16-16t64 libpcre2-16-0 zlib1g libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/qt /work/qt
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENV LD_LIBRARY_PATH=/work/qt/lib
ENTRYPOINT ["/work/run-control.sh"]
