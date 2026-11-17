FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '946168c73e767114e48db94ebf22aa7126af1f9ed2a4edcaee73f10179bf63a5  /go/pkg/mod/cache/download/github.com/mmcdole/goxpp/@v/v1.3.0.zip' | sha256sum --check \
    && echo '41a7f2c7c910a57f70ce460cbe057a31703e11dbb169b499e50a3339a5f33bdb  /usr/local/go/src/encoding/xml/xml.go' | sha256sum --check \
    && echo '0855d63ac5b66f94ad3daca8c2e6d4f70cd8922e9ba67ce00dbc6f35b498623d  /go/pkg/mod/github.com/mmcdole/goxpp@v1.3.0/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/mmcdole/goxpp,encoding/xml -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
