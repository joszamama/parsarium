FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '35ddd96302903cb940e9cfe0acc8b04ccfadce7561daf4caf58a9a0ca30e4213  /go/pkg/mod/cache/download/github.com/gen2brain/go-unarr/@v/v0.2.4.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=1 go test -c -coverpkg=github.com/gen2brain/go-unarr -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM --platform=linux/arm64 debian@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
