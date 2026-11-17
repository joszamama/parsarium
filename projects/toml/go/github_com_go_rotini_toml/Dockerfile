FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '7d62174285d504ca2c22c94dd7d6ef403a3ea902c85a742f04148ed157e035f7  /go/pkg/mod/cache/download/github.com/go-rotini/toml/@v/v1.2.2.zip' | sha256sum --check \
    && echo '920b3c8f78aa5a5e39ed929c13a97fb6e99b02fa08d35406fe911b3474b17944  /go/pkg/mod/github.com/go-rotini/toml@v1.2.2/parser.go' | sha256sum --check \
    && echo '891c79c26e96bbddc97ed145d2f3bcce12c021c783f53dda4a6c514b6157cf93  /go/pkg/mod/github.com/go-rotini/toml@v1.2.2/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/go-rotini/toml -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
