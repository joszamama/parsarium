FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
RUN echo '1675694ef690db0f18fbe7046a886170904bede1d9db6ec96ae27945c1705c64  /usr/local/go/bin/go' | sha256sum --check \
    && echo '0b32a0b4ee51e00e3410764f3b2ffe1163dccb9cad548b097f47db85893a2f44  /usr/local/go/src/net/http/response.go' | sha256sum --check
COPY go.mod ./
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=net/http -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter
FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
