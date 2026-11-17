FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'ea316eb3583417e9864e423d0ed5d1ace8d615a13450c5ea4dc814ab84455209  /go/pkg/mod/cache/download/github.com/phuslu/fastdns/@v/v0.17.2.zip' | sha256sum --check \
    && grep -q 'Permission is hereby granted' /go/pkg/mod/github.com/phuslu/fastdns@v0.17.2/LICENSE
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/phuslu/fastdns -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
