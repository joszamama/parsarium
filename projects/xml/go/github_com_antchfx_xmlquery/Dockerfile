FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'cdb7830a6e1e3f52c3d3a084b55b4bdf84f73b8073c582bca8f5f00d15a5f94c  /go/pkg/mod/cache/download/github.com/antchfx/xmlquery/@v/v1.5.2.zip' | sha256sum --check \
    && echo '41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb  /usr/local/go/src/encoding/xml/xml.go' | sha256sum --check \
    && echo 'c181eed254a608399a1059ddf5cb72cb1f1a5841a083aaa30f3e6713853ddf9f  /go/pkg/mod/github.com/antchfx/xmlquery@v1.5.2/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/antchfx/xmlquery,encoding/xml -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
