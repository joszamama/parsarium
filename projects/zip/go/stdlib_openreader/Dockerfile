FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
RUN echo '1675694ef690db0f18fbe7046a886170904bede1d9db6ec96ae27945c1705c64  /usr/local/go/bin/go' | sha256sum --check \
    && echo 'd35e8e55c85c222c16b29f8976a51698533c3874ff478427794a29af7b23e417  /usr/local/go/src/archive/zip/reader.go' | sha256sum --check
COPY go.mod ./
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=archive/zip -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter
FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
