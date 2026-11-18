FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '02af96f916d1f2c00ed6f10c5bc12a38340a83da0711c7912be8c4be4de70c6d  /go/pkg/mod/cache/download/github.com/shadowy-pycoder/mshark/@v/v0.0.32.zip' | sha256sum --check \
    && grep -q 'Permission is hereby granted' /go/pkg/mod/github.com/shadowy-pycoder/mshark@v0.0.32/LICENSE
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/shadowy-pycoder/mshark/layers -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
