FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download go.viam.com/rdk github.com/chenzhekl/goply \
    && echo '0051f38111c07adcf9c5780c4091b4d3ed21c92077049f7bbfc932bc99a7fade  /go/pkg/mod/cache/download/go.viam.com/rdk/@v/v1.17.0.zip' | sha256sum --check \
    && echo '925fd1588d8a0c5398f3d51326e7e9c8d384bc88ec093bd49426a5c5511fd927  /go/pkg/mod/cache/download/github.com/chenzhekl/goply/@v/v0.0.0-20190930133256-258c2381defd.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=go.viam.com/rdk/spatialmath,github.com/chenzhekl/goply -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
