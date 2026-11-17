FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/xwb1989/sqlparser \
    && echo '9ebb970f2006a76b86f8cfb4fe58e3618d6a37055dd1f70a4f1415d428dba728  /go/pkg/mod/cache/download/github.com/xwb1989/sqlparser/@v/v0.0.0-20180606152119-120387863bf2.zip' | sha256sum --check \
    && echo '43070e2d4e532684de521b885f385d0841030efa2b1a20bafb76133a5e1379c1  /go/pkg/mod/github.com/xwb1989/sqlparser@v0.0.0-20180606152119-120387863bf2/LICENSE.md' | sha256sum --check
COPY harness.go harness_test.go ./
COPY replay/main.go ./replay/main.go
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/xwb1989/sqlparser -o /work/harness.test . \
    && CGO_ENABLED=0 go build -o /work/replay-bin ./replay
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/replay-bin /work/replay
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
