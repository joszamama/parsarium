FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/cockroachdb/cockroachdb-parser \
    && echo 'e576898c2c400b4f543a6c4a8ebdb474bc5b042b917887b1a6e64e567073ae1f  /go/pkg/mod/cache/download/github.com/cockroachdb/cockroachdb-parser/@v/v0.25.2.zip' | sha256sum --check \
    && echo 'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30  /go/pkg/mod/github.com/cockroachdb/cockroachdb-parser@v0.25.2/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
COPY replay/main.go ./replay/main.go
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/cockroachdb/cockroachdb-parser/pkg/sql/parser,github.com/cockroachdb/cockroachdb-parser/pkg/sql/scanner -o /work/harness.test . \
    && CGO_ENABLED=0 go build -o /work/replay-bin ./replay
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/replay-bin /work/replay
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
