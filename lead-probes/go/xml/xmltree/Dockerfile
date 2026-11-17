FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '3aeea5b001f81a6e3cdc857daab12d165cf63b39235bf5f09a5d822ab5816f63  /go/pkg/mod/cache/download/aqwari.net/xml/@v/v0.0.0-20210331023308-d9421b293817.zip' | sha256sum --check \
    && echo '6c932ebde0dc22d8bf15da1597caff3edc0a7c3d58b3228577fe34549af8aede  /go/pkg/mod/aqwari.net/xml@v0.0.0-20210331023308-d9421b293817/xmltree/xmltree.go' | sha256sum --check \
    && echo '9b22159825e3ab7a4c246ace20e19b5aad02d2d2a2f74f75dcca0e1050261278  /go/pkg/mod/aqwari.net/xml@v0.0.0-20210331023308-d9421b293817/LICENSE' | sha256sum --check \
    && echo '6f8a42de5eac02318efa7ffbe53bef9be7aea7434f3f2214867545d2934c2c06  /go/pkg/mod/cache/download/golang.org/x/net/@v/v0.0.0-20200813134508-3edf25e44fcc.zip' | sha256sum --check \
    && echo 'ea3068395503d3c7ef8ce16a286f75c8c93882c25a66c2aa6c8e2ad4da7a9ae0  /go/pkg/mod/cache/download/golang.org/x/text/@v/v0.3.0.zip' | sha256sum --check \
    && echo '41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb  /usr/local/go/src/encoding/xml/xml.go' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=aqwari.net/xml/xmltree,encoding/xml -o /work/harness.test .

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
ENTRYPOINT ["/work/harness.test"]
