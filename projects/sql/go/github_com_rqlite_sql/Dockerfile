FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/rqlite/sql \
    && echo '826738822b97cb48a38f4ea98f5996cdd9b12c573bdcd2639ec7fbe51d5dffec  /go/pkg/mod/cache/download/github.com/rqlite/sql/@v/v0.0.0-20261016220845-5c0832fea6e1.zip' | sha256sum --check \
    && echo '30364cd71656839f9bddeebc791e4eba6ef87b31fe7eb25371baee380f2b62ea  /go/pkg/mod/github.com/rqlite/sql@v0.0.0-20261016220845-5c0832fea6e1/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
COPY replay/main.go ./replay/main.go
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/rqlite/sql -o /work/harness.test . \
    && CGO_ENABLED=0 go build -o /work/replay-bin ./replay
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/replay-bin /work/replay
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
