FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'ce046c493b4b8c120dd0d7eda0a2f255c5206293a7bd8d1bce9f8bcd06b2e504  /go/pkg/mod/cache/download/github.com/cobaltgray/go-plyfile/@v/v0.0.0-20210513130740-b21b0efca069.zip' | sha256sum --check
RUN cd /go/pkg/mod/github.com/cobaltgray/go-plyfile@v0.0.0-20210513130740-b21b0efca069/lib && make all
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=1 go test -c -coverpkg=github.com/cobaltgray/go-plyfile -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
