FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/icculus/SDL_sound/releases/download/v3.2.0/SDL3_sound-3.2.0.tar.gz -o /work/source.tar.gz \
 && echo '3348f3ecc653e21f2b7ed8e409f07c67b179fbbfba3b99c85698e6e5d7b5924c  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
 && curl --fail --location --retry 3 https://github.com/libsdl-org/SDL/releases/download/release-3.4.20/SDL3-3.4.20.tar.gz -o /work/sdl-source.tar.gz \
 && echo 'f3bb06f55bed9557227a700af2ea62e49497ebdf58037732a731a5fb3ef8581f  /work/sdl-source.tar.gz' | sha256sum --check \
 && mkdir /work/sdl-source && tar -xzf /work/sdl-source.tar.gz -C /work/sdl-source --strip-components=1
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang --version | head -1; llvm-cov --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends llvm python3 libstdc++6 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/source /work/source
COPY --from=build /work/sdl-source /work/sdl-source
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
