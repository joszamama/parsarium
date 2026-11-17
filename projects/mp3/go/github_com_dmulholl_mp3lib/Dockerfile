FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'c29d82de91787cc30c6bc9c6a5d5b14e203f8765563de23aa2c242f54c3ea1d9  /go/pkg/mod/cache/download/github.com/dmulholl/mp3lib/@v/v1.0.0.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/dmulholl/mp3lib -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
