FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
ENV GOTOOLCHAIN=auto
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '7845e9cffe069fcd7e7be32d1abbbb11553ea8a1ba8e062a5542ad4ee12aa2a2  /go/pkg/mod/cache/download/github.com/pdfcpu/pdfcpu/@v/v0.16.4.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/pdfcpu/pdfcpu/pkg/api -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
ENV XDG_CONFIG_HOME=/tmp
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
