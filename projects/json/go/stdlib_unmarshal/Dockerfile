FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
RUN echo '1675694ef690db0f18fbe7046a886170904bede1d9db6ec96ae27945c1705c64  /usr/local/go/bin/go' | sha256sum --check \
    && echo 'd82e2e8ac32bc64c967b02769fc1fc6e2e5e9d7aae384673709e6af4669bc3fe  /usr/local/go/src/encoding/json/v2_decode.go' | sha256sum --check \
    && echo '6978277353d629e9fa02a3a351df55d647a067918c33fff6617ccaf307656fc8  /usr/local/go/src/encoding/json/jsontext/decode.go' | sha256sum --check \
    && echo '54dc9704a72fe6836422f3ca4a216d32c55e5ffdf964c84ccb868e171997d5eb  /usr/local/go/src/encoding/json/v2/arshal.go' | sha256sum --check
COPY go.mod ./
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=encoding/json/... -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter
FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
