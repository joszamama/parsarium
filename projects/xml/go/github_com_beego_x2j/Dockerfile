FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'f9a32026b2107f3cc3610ac6b75c4c64818646a316c35e648c8811d4276a9993  /go/pkg/mod/cache/download/github.com/beego/x2j/@v/v0.0.0-20131220205130-a0352aadc542.zip' | sha256sum --check \
    && echo '6aedea13b75e3f84d6740918d98bcbe7b2671472dbe372d8214f4bf95869dfcc  /go/pkg/mod/github.com/beego/x2j@v0.0.0-20131220205130-a0352aadc542/x2j.go' | sha256sum --check \
    && echo 'a6667e67d1e25f20ae40e0ccf1bde31e2a557e440a6d3f74ec327d20d795cc7f  /go/pkg/mod/github.com/beego/x2j@v0.0.0-20131220205130-a0352aadc542/reader2j.go' | sha256sum --check \
    && echo '9ac1a4cd3ea86997440deabc5c1491af6c0c75dfa47175f35de2cbd22cf5ec00  /go/pkg/mod/github.com/beego/x2j@v0.0.0-20131220205130-a0352aadc542/LICENSE' | sha256sum --check \
    && echo '41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb  /usr/local/go/src/encoding/xml/xml.go' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/beego/x2j,encoding/xml -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
