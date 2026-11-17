FROM --platform=linux/arm64 parsarium/sql-go-github_com_pganalyze_pg_query_go_v6:local
RUN apt-get update -qq && apt-get install -y --no-install-recommends afl++=4.04c-4 \
    && rm -rf /var/lib/apt/lists/*
COPY afl-allowlist.txt /work/afl-allowlist.txt
# Only the bundled libpg_query grammar (bison), scanner (flex) and parser.c driver are
# instrumented; the Go runtime, the protobuf output path and the Go tree walk are not.
RUN go clean -cache \
    && AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt AFL_LLVM_INSTRUMENT=CLASSIC \
       CC=afl-clang-fast CGO_CFLAGS='-O1 -g -fno-omit-frame-pointer' CGO_LDFLAGS='' \
       go build -tags afl -o /work/afl-target ./replay
ENTRYPOINT ["/work/afl-target"]
