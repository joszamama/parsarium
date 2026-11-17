FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '8947cf617bdd9efc62817c8ddb17bafe497f35abdf10a3c60f295e387f633f70  /go/pkg/mod/cache/download/github.com/clbanning/mxj/@v/v1.8.4.zip' | sha256sum --check \
    && echo '944ce03ae64b1d93742e8c94030951ca26f0a8c18ffc158935f393b3a6c39def  /go/pkg/mod/github.com/clbanning/mxj@v1.8.4/xml.go' | sha256sum --check \
    && echo 'b8eff858879438dbaefa6f153553230337c4776a861b8d658f295636a88050ec  /go/pkg/mod/github.com/clbanning/mxj@v1.8.4/LICENSE' | sha256sum --check \
    && echo '41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb  /usr/local/go/src/encoding/xml/xml.go' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/clbanning/mxj,encoding/xml -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
