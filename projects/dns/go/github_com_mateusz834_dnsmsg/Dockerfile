FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '5625dd9c0c4b3d3c6f615ce0c125e6dcf48a2bc3982d8bb0189ba5187e103c9a  /go/pkg/mod/cache/download/github.com/mateusz834/dnsmsg/@v/v0.0.0-20231225175121-c6b857669b66.zip' | sha256sum --check \
    && grep -q 'Permission is hereby granted' /go/pkg/mod/github.com/mateusz834/dnsmsg@v0.0.0-20231225175121-c6b857669b66/LICENSE
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/mateusz834/dnsmsg -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
