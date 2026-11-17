# Build after the pinned CPython/Tk control image has been verified locally.
FROM --platform=linux/arm64 parsarium/png-python-stdlib_tkinter_photoimage:local AS build
ENV DEBIAN_FRONTEND=noninteractive AFL_LLVM_INSTRUMENT=CLASSIC
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 ca-certificates clang curl libclang-rt-21-dev \
    make pkg-config tcl8.6-dev tk8.6-dev libx11-dev libxext-dev libxft-dev \
    libxss-dev libxrender-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 \
    https://downloads.sourceforge.net/project/tcl/Tcl/8.6.16/tk8.6.16-src.tar.gz \
    -o /work/tk-afl.tar.gz \
    && echo 'be9f94d3575d4b3099d84bc3c10de8994df2d7aa405208173c709cc404a7e5fe  /work/tk-afl.tar.gz' | sha256sum --check \
    && mkdir /work/tk-afl-source \
    && tar -xf /work/tk-afl.tar.gz -C /work/tk-afl-source --strip-components=1 \
    && echo '183dcf8948132893a3d232ab4c321e86bc32e05656d0771873fa48939399fa48  /work/tk-afl-source/generic/tkImgPNG.c' | sha256sum --check
RUN printf 'src:tkImgPNG.c\n' > /work/afl-allowlist.txt \
    && tk_config=$(dpkg -L tcl8.6-dev | grep '/tclConfig.sh$' | head -1) \
    && test -n "$tk_config" \
    && cd /work/tk-afl-source/unix \
    && CC=afl-clang-fast \
       CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' \
       AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt \
       ./configure --prefix=/opt/tk-afl --with-tcl="$(dirname "$tk_config")" --enable-shared \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt make -j 4 \
    && make install \
    && echo '183dcf8948132893a3d232ab4c321e86bc32e05656d0771873fa48939399fa48  /work/tk-afl-source/generic/tkImgPNG.c' | sha256sum --check \
    && { afl-clang-fast --version | head -1; llvm-cov --version | head -1; } > /work/feedback-toolchain.txt
COPY launcher.c /work/launcher.c
RUN clang -O1 -g /work/launcher.c /usr/lib/afl/afl-compiler-rt.o \
    -L/opt/python/lib -lpython3.13 -Wl,-rpath,/opt/python/lib \
    -Wl,--export-dynamic -o /work/afl-python

FROM --platform=linux/arm64 parsarium/png-python-stdlib_tkinter_photoimage:local
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    afl++=4.33c-1.1ubuntu1 && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/tk-afl /opt/tk-afl
COPY --from=build /work/tk-afl-source/generic/tkImgPNG.c /work/tk-afl-source/generic/tkImgPNG.c
COPY --from=build /work/feedback-toolchain.txt /work/feedback-toolchain.txt
COPY --from=build /work/afl-python /work/afl-python
COPY showmap.sh with-display.sh /work/
RUN chmod +x /work/showmap.sh /work/with-display.sh
ENV LD_LIBRARY_PATH=/opt/tk-afl/lib:/opt/python/lib
ENV TK_LIBRARY=/opt/tk/lib/tk8.6
ENV AFL_PRELOAD=/opt/tk-afl/lib/libtk8.6.so
ENV LLVM_PROFILE_FILE=/dev/null
ENTRYPOINT ["/work/with-display.sh", "/work/afl-python", "/work/replay.py"]
