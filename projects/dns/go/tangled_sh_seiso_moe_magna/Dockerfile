FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'b1951fc60696ed08998cfbfb624ef5a5fceab5aadb2c2745204b7db5b9da97aa  /go/pkg/mod/cache/download/tangled.sh/seiso.moe/magna/@v/v0.0.2.zip' | sha256sum --check \
    && grep -q 'Permission is hereby granted' /go/pkg/mod/tangled.sh/seiso.moe/magna@v0.0.2/LICENSE
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=tangled.sh/seiso.moe/magna -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
