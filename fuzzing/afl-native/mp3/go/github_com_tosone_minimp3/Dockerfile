# Native AFL++ overlay: only the vendored minimp3 C decoder is instrumented.
FROM --platform=linux/arm64 parsarium/mp3-go-github_com_tosone_minimp3:local
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.04c-4 \
    && rm -rf /var/lib/apt/lists/*
COPY afl-allowlist.txt /work/allowlist
COPY cmd/afl-target/main.go /work/cmd/afl-target/main.go
RUN AFL_LLVM_ALLOWLIST=/work/allowlist AFL_LLVM_INSTRUMENT=CLASSIC \
    CC=afl-clang-fast CGO_ENABLED=1 go build -o /work/afl-target ./cmd/afl-target
ENTRYPOINT ["/work/afl-target"]
