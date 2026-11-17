FROM --platform=linux/arm64 parsarium/xml-go-github_com_lestrrat_go_libxml2:local
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.04c-4 \
    && rm -rf /var/lib/apt/lists/*
COPY afl-allowlist.txt /work/afl-allowlist.txt
COPY cmd/parse-only/main.go /work/cmd/parse-only/main.go
RUN cd /work/libxml2-source \
    && make distclean \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       CC=afl-clang-fast CFLAGS='-O1 -g -fno-omit-frame-pointer' ./configure \
       --prefix=/opt/libxml2 --disable-shared --enable-static --without-python \
       --without-zlib --without-lzma --without-iconv --without-icu --without-http \
       --without-modules --without-catalog \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       make -j4 && make install
RUN go clean -cache \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       CC=afl-clang-fast CGO_LDFLAGS='-lm' go build -tags afl -o /work/afl-target ./cmd/replay \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       CC=afl-clang-fast CGO_LDFLAGS='-lm' go build -tags afl -o /work/parse-only ./cmd/parse-only
ENTRYPOINT ["/work/afl-target"]
