FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
 ca-certificates clang cmake curl libclang-rt-21-dev llvm make python3 \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/Exiv2/exiv2/archive/refs/tags/v0.28.9.tar.gz -o /work/source.tar.gz \
 && echo '700b76b97695b2fab4ef8c79619c68ae57d09e0c130724791cafbd39e0eb4aef  /work/source.tar.gz' | sha256sum --check \
 && tar -xzf /work/source.tar.gz -C /work \
 && cd /work/exiv2-0.28.9 && printf '%s\n' \
 '0694c5ce823c53929a09758f570f592362ccde4e6af27fd1691794c309a281c6  src/quicktimevideo.cpp' \
 '7e11bcfc4aa6e83ecd8e737aa305c4bf2f3d549a7977852ff9fa965509b89772  include/exiv2/quicktimevideo.hpp' \
 '692a02bcd1977b4621301e18ae8661a6297a5c7abf06f50d4b6fd45554b063f2  src/image.cpp' \
 '89d465f195320eb683d7b20f58c3089b05596edd282e10af9cd62bf366feae44  src/basicio.cpp' \
 'f1652310b8b61f4a916bc3967504714837393ce21043f4f7fa5bf1b17baa3e51  src/xmp.cpp' \
 '5ee5c94376ef8ff0fb0396fe43f642c4b1945ea001ec6dd3e9f6dcb7f508764a  include/exiv2/exiv2.hpp' \
 'a7ba75cb966aca374711e2af49e5f3aea6a4443a803440f5d93e73a5a1222f66  COPYING' \
 | sha256sum --check
COPY harness.cpp harness.h replay.cpp build.sh /work/
RUN chmod +x /work/build.sh && /work/build.sh \
 && { clang++ --version | head -1; llvm-cov --version | head -1; cmake --version | head -1; } > /work/toolchain.txt
FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
 libstdc++6 llvm python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/replay /work/fuzzer /work/
COPY --from=build /work/exiv2-0.28.9/src /work/exiv2-0.28.9/src
COPY --from=build /work/exiv2-0.28.9/include /work/exiv2-0.28.9/include
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY run-control.sh /work/run-control.sh
RUN chmod +x /work/run-control.sh
ENTRYPOINT ["/work/run-control.sh"]
