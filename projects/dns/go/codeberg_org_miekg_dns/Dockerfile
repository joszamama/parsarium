FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '0999540989d9a357ed6fd8833ea20beefb6641beffb2d75d16b2a9acaff7a8c8  /go/pkg/mod/cache/download/codeberg.org/miekg/dns/@v/v0.6.133.zip' | sha256sum --check \
    && grep -q 'Redistribution and use in source and binary forms' /go/pkg/mod/codeberg.org/miekg/dns@v0.6.133/LICENSE
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=codeberg.org/miekg/dns,codeberg.org/miekg/dns/internal/unpack,codeberg.org/miekg/dns/internal/dnsstring,codeberg.org/miekg/dns/pkg/dnsnet,codeberg.org/miekg/dns/rdata -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
