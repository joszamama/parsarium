FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'fc8cbe2239683199e677cb39f9303ae8d4a365f3c8cd8a2dcfa1f14c41bcff88  /go/pkg/mod/cache/download/github.com/google/gopacket/@v/v1.1.19.zip' | sha256sum --check \
    && grep -q 'Redistribution and use in source and binary forms' /go/pkg/mod/github.com/google/gopacket@v1.1.19/LICENSE
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/google/gopacket/layers -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
