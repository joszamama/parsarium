FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
ENV GOTOOLCHAIN=auto
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'af2ddb8d8d068f5734aad557f775c58774befe4986f0cf27a8417be66d1df552  /go/pkg/mod/cache/download/github.com/giraffesyo/pdf/@v/v0.9.0.zip' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/giraffesyo/pdf -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
