FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '7e1e3ef1d734ed06002675b07855b878aed84b840eae6ae066297bb3159e132a  /go/pkg/mod/cache/download/github.com/benburkert/dns/@v/v0.0.0-20190225204957-d356cf78cdfc.zip' | sha256sum --check \
    && grep -q 'Permission is hereby granted' /go/pkg/mod/github.com/benburkert/dns@v0.0.0-20190225204957-d356cf78cdfc/LICENSE
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/benburkert/dns -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
