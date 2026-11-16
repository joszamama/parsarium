FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends libvips-dev pkg-config && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '9baeee2c0f7b6c616bac4217b740b0c13a88fd4857d2463837ab170746be359c  /go/pkg/mod/cache/download/github.com/davidbyttow/govips/v2/@v/v2.20.0.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=1 go test -c -coverpkg=github.com/davidbyttow/govips/v2/vips -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
RUN apt-get update -qq && apt-get install -y --no-install-recommends libvips42 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
