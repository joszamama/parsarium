FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/yongjohnlee80/golib \
    && echo '19aa57b9e220858d7cfae9759b4c4832cbfc67175aec385cda88dc5dbc8bc57c  /go/pkg/mod/cache/download/github.com/yongjohnlee80/golib/@v/v0.8.62.zip' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/yongjohnlee80/golib/parse/yaml,github.com/yongjohnlee80/golib/yaml -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
