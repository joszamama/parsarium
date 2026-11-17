FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'bac58029d1dfabc68af13a8119c776e1d10dc2ede26039588fd1f9527b939624  /go/pkg/mod/cache/download/github.com/bytedance/sonic/@v/v1.15.5.zip' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/bytedance/sonic/... -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
