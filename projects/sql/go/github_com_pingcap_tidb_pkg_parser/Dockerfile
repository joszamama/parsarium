FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
ENV GOTOOLCHAIN=auto
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/pingcap/tidb/pkg/parser \
    && echo '0c1a8be16c91cd96292df2c50158a8c817c59bffdcb4a13b6b57e2e6f8b591e3  /go/pkg/mod/cache/download/github.com/pingcap/tidb/pkg/parser/@v/v0.0.0-20261117145351-1e84b3595a3e.zip' | sha256sum --check \
    && echo 'c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4  /go/pkg/mod/github.com/pingcap/tidb/pkg/parser@v0.0.0-20261117145351-1e84b3595a3e/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
COPY replay/main.go ./replay/main.go
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/pingcap/tidb/pkg/parser -o /work/harness.test . \
    && CGO_ENABLED=0 go build -o /work/replay-bin ./replay
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/replay-bin /work/replay
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
