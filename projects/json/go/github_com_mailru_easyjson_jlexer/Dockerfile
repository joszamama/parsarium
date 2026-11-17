FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'b9df0a16e05ca83bd12e36f11fb6d35622fffdda8d18b83ab7c030d11903af73  /go/pkg/mod/cache/download/github.com/mailru/easyjson/@v/v0.9.2.zip' | sha256sum --check \
    && echo '5679bfd11c14adccdb45bd1a0f9cf4b445b95caeed6fb507ba96ecced11c248d  /go/pkg/mod/cache/download/github.com/josharian/intern/@v/v1.0.0.zip' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/mailru/easyjson/jlexer -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
