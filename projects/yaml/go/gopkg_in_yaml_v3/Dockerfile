FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download gopkg.in/yaml.v3 \
    && echo 'aab8fbc4e6300ea08e6afe1caea18a21c90c79f489f52c53e2f20431f1a9a015  /go/pkg/mod/cache/download/gopkg.in/yaml.v3/@v/v3.0.1.zip' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=gopkg.in/yaml.v3/... -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
