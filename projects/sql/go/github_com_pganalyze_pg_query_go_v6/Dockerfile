FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    clang libclang-rt-14-dev llvm python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY go.mod go.sum ./
# pg_query_go bundles the libpg_query C sources in parser/. The bison/flex outputs carry #line
# directives to gram.y and scan.l, which are not shipped; they are removed from a copy of the
# pinned module so Clang coverage is attributed to the pinned C files.
RUN go mod download \
    && echo '3177b3123f142e58febadab2ccbb6b0df1536fff41ffaccb4112c1422e4dc92a  /go/pkg/mod/cache/download/github.com/pganalyze/pg_query_go/v6/@v/v6.2.5.zip' | sha256sum --check \
    && echo '7752b24a3cb4bee5270c2ee8a3a7609fd57ce9dccb2e8b5757fdeca04bb03960  /go/pkg/mod/github.com/pganalyze/pg_query_go/v6@v6.2.5/LICENSE' | sha256sum --check \
    && echo '28e429702de70abfa1b7e4cb5d9e486bd9469f1eab5b392f704b65de09334d8d  /go/pkg/mod/github.com/pganalyze/pg_query_go/v6@v6.2.5/LICENSE.POSTGRESQL' | sha256sum --check \
    && cp -a /go/pkg/mod/github.com/pganalyze/pg_query_go/v6@v6.2.5 /work/thirdparty \
    && chmod -R u+w /work/thirdparty \
    && sed -i '/^#line /d' /work/thirdparty/parser/src_backend_parser_gram.c /work/thirdparty/parser/src_backend_parser_scan.c \
    && go mod edit -replace github.com/pganalyze/pg_query_go/v6=/work/thirdparty
ENV CC=clang
ENV CGO_ENABLED=1
ENV CGO_CFLAGS="-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping"
ENV CGO_LDFLAGS=-fprofile-instr-generate
COPY harness.go harness_test.go native_profile.go native_profile_afl.go report.py ./
COPY replay/main.go ./replay/main.go
RUN go test -c -coverpkg=github.com/pganalyze/pg_query_go/v6,github.com/pganalyze/pg_query_go/v6/parser -o /work/harness.test . \
    && go build -o /work/replay-bin ./replay
ENTRYPOINT ["python3", "/work/report.py"]
