FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'c0338bfc955c839a435fc49156536be7e39525455412940f12ef1e0a903ee706  /go/pkg/mod/cache/download/github.com/beevik/etree/@v/v1.8.1.zip' | sha256sum --check \
    && echo '41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb  /usr/local/go/src/encoding/xml/xml.go' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/beevik/etree,encoding/xml -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
