FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'b3d1397b93e47bee18034c085c1841691edfcc25971809384ac824c0285da58c  /go/pkg/mod/cache/download/github.com/fogleman/fauxgl/@v/v0.0.0-20250110135958-abf826acbbbd.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/fogleman/fauxgl -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
