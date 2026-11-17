FROM --platform=linux/arm64 parsarium/ascii_pnm-go-github_com_cshum_vipsgen_vips:local
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.04c-4 \
    && rm -rf /var/lib/apt/lists/*
COPY afl-allowlist.txt /work/afl-allowlist.txt
RUN rm -rf /opt/vips && cd /work/vips-source \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       CC=afl-clang-fast CXX=afl-clang-fast++ CFLAGS='-O1 -g -fno-omit-frame-pointer' \
       CXXFLAGS='-O1 -g -fno-omit-frame-pointer' meson setup build-afl $VIPS_MESON \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       ninja -C build-afl && ninja -C build-afl install \
    && sed -i "$VIPS_PC_FIX" /opt/vips/lib/pkgconfig/vips.pc
RUN go clean -cache \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       CC=afl-clang-fast CGO_LDFLAGS='' go build -tags afl -o /work/afl-target ./cmd/replay \
    && nm /work/afl-target | grep -q '__afl_area_ptr' \
    && nm /work/afl-target | grep -q ' vips_foreign_load_ppm_buffer_build$'
ENTRYPOINT ["/work/afl-target"]
