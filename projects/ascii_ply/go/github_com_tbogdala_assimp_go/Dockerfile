FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends libassimp-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '991af2ea50947277362373deee14cac594d61ea36619730c3a88087f77aa7cfc  /go/pkg/mod/cache/download/github.com/tbogdala/assimp-go/@v/v0.0.0-20160907223021-d10e2135f9fe.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=1 go test -c -coverpkg=github.com/tbogdala/assimp-go -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM --platform=linux/arm64 debian@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc
RUN apt-get update -qq && apt-get install -y --no-install-recommends libassimp5 && rm -rf /var/lib/apt/lists/*
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
