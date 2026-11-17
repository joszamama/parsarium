FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '522bb51d5a44baefef0e0895b5e33fcf4d003058aeada5cdf41f2ef07c05f926  /go/pkg/mod/cache/download/github.com/go-faster/jx/@v/v1.2.0.zip' | sha256sum --check \
    && echo 'de12a734468634ef76f07788b5fe464d4fcb09f56cede6a3187720a256aa0ad4  /go/pkg/mod/cache/download/github.com/go-faster/errors/@v/v0.7.1.zip' | sha256sum --check \
    && echo '04ee03ed0972329c3c8fa1cd57a30397be37b82f3e2ba2251d56ba9c6fbc1d99  /go/pkg/mod/cache/download/github.com/segmentio/asm/@v/v1.2.1.zip' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/go-faster/jx -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
