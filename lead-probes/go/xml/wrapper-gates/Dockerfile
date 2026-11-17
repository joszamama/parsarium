FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '2f7b5f64b31f00193bf1a848d2aacf9d2a555f22076d52c31957c59d7a20ca77  /go/pkg/mod/cache/download/github.com/basgys/goxml2json/@v/v1.1.0.zip' | sha256sum --check \
    && echo '0b3c16a209b3a8a9e9b76b9b1f77cf7d01db9f0f830a20a2e9b5d7f0ebbd2282  /go/pkg/mod/cache/download/github.com/!victor!lowther/simplexml/@v/v0.0.0-20180716164440-0bff93621230.zip' | sha256sum --check \
    && echo 'd29d651d8e63d4b90b9245c923f8d0c3ee670bd7481d3830ebd4853e41df9fd7  /go/pkg/mod/cache/download/github.com/subchen/go-xmldom/@v/v1.1.2.zip' | sha256sum --check \
    && echo 'e517e16d8e4e3554d9ada26547bb8df77bb96d39ecf1952b67e4aad392734092  /go/pkg/mod/cache/download/github.com/sbabiv/xml2map/@v/v1.2.1.zip' | sha256sum --check \
    && echo 'fc0597fa42a251b1c4f5edb46df624a4706470fb9af182bb14af328f9258f679  /go/pkg/mod/cache/download/github.com/dgrr/quickxml/@v/v0.0.0-20201022091424-4977de546d6c.zip' | sha256sum --check \
    && echo '41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb  /usr/local/go/src/encoding/xml/xml.go' | sha256sum --check
COPY probe_test.go ./
# One test binary per lead; each instruments only that lead's own package.
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/basgys/goxml2json -o /work/goxml2json.test . \
    && CGO_ENABLED=0 go test -c -coverpkg=github.com/VictorLowther/simplexml/dom -o /work/simplexml-dom.test . \
    && CGO_ENABLED=0 go test -c -coverpkg=github.com/subchen/go-xmldom -o /work/go-xmldom.test . \
    && CGO_ENABLED=0 go test -c -coverpkg=github.com/sbabiv/xml2map -o /work/xml2map.test . \
    && CGO_ENABLED=0 go test -c -coverpkg=github.com/dgrr/quickxml -o /work/quickxml.test .

FROM scratch
COPY --from=build /work/*.test /work/
