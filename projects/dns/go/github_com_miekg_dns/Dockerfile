FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'bbed3c53b503db53002598615bf9bdb59918a6f9d72bd9151e0c52ab19e22a6f  /go/pkg/mod/cache/download/github.com/miekg/dns/@v/v1.1.73.zip' | sha256sum --check \
    && grep -q 'Redistribution and use in source and binary forms' /go/pkg/mod/github.com/miekg/dns@v1.1.73/LICENSE
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/miekg/dns -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
