FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '6f41d156f61d8227f10b40bce8ec124fcedf3d0a3dc30387ff36e3823d3f84d7  /go/pkg/mod/cache/download/github.com/faiface/beep/@v/v1.1.0.zip' | sha256sum --check \
    && echo '6a882c1cad1fc23b9b20add4a5bdc78451378232d630ddcdeac7505f970391be  /go/pkg/mod/cache/download/github.com/hajimehoshi/go-mp3/@v/v0.3.0.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/faiface/beep/mp3,github.com/hajimehoshi/go-mp3/... -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
