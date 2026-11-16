FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS go_toolchain
FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
COPY --from=go_toolchain /usr/local/go /usr/local/go
ENV GOPATH=/go PATH="/usr/local/go/bin:${PATH}"
RUN apt-get update -qq && apt-get install -y --no-install-recommends ca-certificates gcc libc6-dev libmagickwand-dev pkg-config && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '0e5729d2942fef72cc4513b404c0e3e06068899d933814c9c70b2c0643007c05  /go/pkg/mod/cache/download/gopkg.in/gographics/imagick.v3/@v/v3.7.3.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=1 go test -c -coverpkg=gopkg.in/gographics/imagick.v3/imagick -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
RUN apt-get update -qq && apt-get install -y --no-install-recommends libmagickwand-7.q16-10 && rm -rf /var/lib/apt/lists/*
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
