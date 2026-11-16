FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'd56d13bf912ee76d1f3930d6c4808d9daa7576387b652a6a75a0869d9c32e8f2  /go/pkg/mod/cache/download/github.com/zhaofenghao/clash/@v/v1.0.14.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=net/http -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
