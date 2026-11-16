FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends libvips-dev pkg-config && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'e76a09d5ec4f61edb0d73dda9eb037129e99ee321208e2641edda75e26318f3b  /go/pkg/mod/cache/download/github.com/bu/govips/@v/v0.0.0-20191224162542-9c70e55b5850.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=1 go test -c -coverpkg=github.com/bu/govips/pkg/vips -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
RUN apt-get update -qq && apt-get install -y --no-install-recommends libvips42 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
