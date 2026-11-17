FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-21-dev make pkg-config tcl8.6-dev tk8.6-dev \
    libx11-dev libxext-dev libxft-dev libxss-dev libxrender-dev \
    zlib1g-dev libffi-dev libssl-dev libbz2-dev liblzma-dev libreadline-dev \
    libsqlite3-dev llvm xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://downloads.sourceforge.net/project/tcl/Tcl/8.6.16/tk8.6.16-src.tar.gz \
    -o /work/tk.tar.gz \
    && echo 'be9f94d3575d4b3099d84bc3c10de8994df2d7aa405208173c709cc404a7e5fe  /work/tk.tar.gz' | sha256sum --check \
    && mkdir /work/tk && tar -xf /work/tk.tar.gz -C /work/tk --strip-components=1 \
    && echo '183dcf8948132893a3d232ab4c321e86bc32e05656d0771873fa48939399fa48  /work/tk/generic/tkImgPNG.c' | sha256sum --check \
    && curl --fail --location --retry 3 \
    https://www.python.org/ftp/python/3.13.1/Python-3.13.1.tar.xz \
    -o /work/python.tar.xz \
    && echo '9cf9427bee9e2242e3877dd0f6b641c1853ca461f39d6503ce260a59c80bf0d9  /work/python.tar.xz' | sha256sum --check \
    && mkdir /work/python && tar -xf /work/python.tar.xz -C /work/python --strip-components=1
COPY build.sh /work/build.sh
RUN chmod +x /work/build.sh && /work/build.sh \
    && { /opt/python/bin/python3.13 --version; llvm-cov --version | head -1; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    libtcl8.6 libx11-6 libxext6 libxft2 libxss1 libxrender1 \
    libfontconfig1 libfreetype6 xvfb xauth llvm \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /opt/tk /opt/tk
COPY --from=build /opt/python /opt/python
COPY --from=build /work/tk/generic/tkImgPNG.c /work/tk/generic/tkImgPNG.c
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY replay.py replay-cli.py run-control.py /work/
ENV LD_LIBRARY_PATH=/opt/tk/lib:/opt/python/lib
ENV LLVM_PROFILE_FILE=/dev/null
ENV TCL_LIBRARY=/usr/share/tcltk/tcl8.6
ENV TK_LIBRARY=/opt/tk/lib/tk8.6
ENTRYPOINT ["/opt/python/bin/python3.13", "/work/run-control.py"]
