FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '20f833eba102520fc4efd0c473fa3591bb098df25422f5b16e802bfcf9f8e16d  /go/pkg/mod/cache/download/github.com/tcolgate/mp3/@v/v0.0.0-20170426193717-e79c5a46d300.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/tcolgate/mp3 -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
