FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'ae7bba276dd08e966b7812c50218ccccd31e090792735f0da97dfa0dafa604e6  /go/pkg/mod/cache/download/github.com/lestrrat-go/helium/@v/v0.11.0.zip' | sha256sum --check \
    && echo 'cd7bdb29c7039a19188d1234d5c93933c432395c319e3c7e4845ad2a0c3063a5  /go/pkg/mod/github.com/lestrrat-go/helium@v0.11.0/parser.go' | sha256sum --check \
    && echo '0c4868a07b1c2dbb67c75767b4f1b2936c392d02ca2c7ee9827cac1a9d60ab1d  /go/pkg/mod/github.com/lestrrat-go/helium@v0.11.0/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
# Instrument helium's root package and the internal parser, SAX and helper packages it links.
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/lestrrat-go/helium/... -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
