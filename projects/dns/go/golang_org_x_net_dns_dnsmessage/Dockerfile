FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'e155ed7fbcd5c8b799daca68c0a7bdf31eb793bda052eda207d1faf25863fffc  /go/pkg/mod/cache/download/golang.org/x/net/@v/v0.63.0.zip' | sha256sum --check \
    && grep -q 'Redistribution and use in source and binary forms' /go/pkg/mod/golang.org/x/net@v0.63.0/LICENSE
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=golang.org/x/net/dns/dnsmessage -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
