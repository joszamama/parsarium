FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/AfterShip/clickhouse-sql-parser \
    && echo '7005b778a6185dc978504403d93d78644df8a31288e130cde04caae012048dd0  /go/pkg/mod/cache/download/github.com/!after!ship/clickhouse-sql-parser/@v/v0.5.7.zip' | sha256sum --check \
    && echo '392a27266877db3e3808ef8bfb6628f1bbb7ee8bef6545e307250a898efd99d8  /go/pkg/mod/github.com/!after!ship/clickhouse-sql-parser@v0.5.7/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
COPY replay/main.go ./replay/main.go
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/AfterShip/clickhouse-sql-parser/parser -o /work/harness.test . \
    && CGO_ENABLED=0 go build -o /work/replay-bin ./replay
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/replay-bin /work/replay
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
