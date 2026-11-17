FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/blastrain/vitess-sqlparser \
    && echo '7511319ea56fb67d02f532e797200075a85660de4b5944de65c7eeb9c574f801  /go/pkg/mod/cache/download/github.com/blastrain/vitess-sqlparser/@v/v0.0.0-20201030050434-a139afbb1aba.zip' | sha256sum --check \
    && echo 'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30  /go/pkg/mod/github.com/blastrain/vitess-sqlparser@v0.0.0-20201030050434-a139afbb1aba/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
COPY replay/main.go ./replay/main.go
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/blastrain/vitess-sqlparser/sqlparser -o /work/harness.test . \
    && CGO_ENABLED=0 go build -o /work/replay-bin ./replay
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/replay-bin /work/replay
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
