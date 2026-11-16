FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/icculus/SDL_sound/releases/download/v2.0.6/SDL2_sound-2.0.6.tar.gz -o /work/source.tar.gz \
 && echo '63be57cc80bcd29aeed6c29700759871c44c90251a7508b8d0eacd8d9cece30c  /work/source.tar.gz' | sha256sum --check \
 && mkdir /work/source && tar -xzf /work/source.tar.gz -C /work/source --strip-components=1 \
 && curl --fail --location --retry 3 https://www.libsdl.org/release/SDL2-2.32.10.tar.gz -o /work/sdl-source.tar.gz \
 && echo '5f5993c530f084535c65a6879e9b26ad441169b3e25d789d83287040a9ca5165  /work/sdl-source.tar.gz' | sha256sum --check \
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
