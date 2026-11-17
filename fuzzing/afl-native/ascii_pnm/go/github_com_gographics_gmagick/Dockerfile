FROM --platform=linux/arm64 parsarium/ascii_pnm-go-github_com_gographics_gmagick:local
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.04c-4 \
    && rm -rf /var/lib/apt/lists/*
COPY afl-allowlist.txt /work/afl-allowlist.txt
RUN rm -rf /opt/gm && cd /work/gm-source \
    && make distclean \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       CC=afl-clang-fast CFLAGS='-O1 -g -fno-omit-frame-pointer' ./configure $GM_CONFIGURE \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       make -j4 && make install \
    && sed -i 's/^Libs: \(.*\)$/Libs: \1 -lm -lpthread/' /opt/gm/lib/pkgconfig/GraphicsMagick.pc /opt/gm/lib/pkgconfig/GraphicsMagickWand.pc
RUN go clean -cache \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       CC=afl-clang-fast CGO_LDFLAGS='' go build -tags afl -o /work/afl-target ./cmd/replay \
    && nm /work/afl-target | grep -q '__afl_area_ptr' \
    && nm /work/afl-target | grep -q ' ReadPNMImage$'
ENTRYPOINT ["/work/afl-target"]
