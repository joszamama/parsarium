FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '8c48f5f6f488c7f79c8f22caedde724bcc77bcc97a9e2d8be5e39f956346fece  /go/pkg/mod/cache/download/github.com/go-forks/go-pkg-xmlx/@v/v0.0.0-20151201012946-76f54ee73233.zip' | sha256sum --check \
    && echo 'ddba522493b65616466a8d913bee214c94dd6cdbdba8481fe8fba9a1e6e7e1cc  /go/pkg/mod/github.com/go-forks/go-pkg-xmlx@v0.0.0-20151201012946-76f54ee73233/document.go' | sha256sum --check \
    && echo 'eb88e5fc39dce2c5abebe2f485ccb5804bc68b151abda7b25e43ad6138f7109a  /go/pkg/mod/github.com/go-forks/go-pkg-xmlx@v0.0.0-20151201012946-76f54ee73233/LICENSE' | sha256sum --check \
    && echo '41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb  /usr/local/go/src/encoding/xml/xml.go' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/go-forks/go-pkg-xmlx,encoding/xml -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
