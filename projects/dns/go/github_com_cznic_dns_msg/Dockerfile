FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '0e8c2eb19f18b36de8991ed4eea957d0dd368e4df905fd0eeeba400358e786af  /go/pkg/mod/cache/download/github.com/cznic/dns/@v/v0.0.0-20181122101858-8a2913d6a50b.zip' | sha256sum --check \
    && grep -q 'Redistribution and use in source and binary forms' /go/pkg/mod/github.com/cznic/dns@v0.0.0-20181122101858-8a2913d6a50b/LICENSE
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/cznic/dns,github.com/cznic/dns/msg,github.com/cznic/dns/rr -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
