FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends libassimp-dev pkg-config && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '511880c15ab0500fdbff419851ab5119835ece013f10f01f03374ec0ffff9ad7  /go/pkg/mod/cache/download/github.com/ajermaky/assimp-go/v2/@v/v2.0.0-20240713211439-0860f3b5f93c.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=1 CGO_LDFLAGS=-lassimp go test -c -coverpkg=github.com/ajermaky/assimp-go/v2/asig -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
RUN apt-get update -qq && apt-get install -y --no-install-recommends libassimp5 && rm -rf /var/lib/apt/lists/*
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
