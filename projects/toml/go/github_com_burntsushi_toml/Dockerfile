FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '01f03d6c3f4bfee108bda3202407b54ac0c295b8302a1315512f12ac05011fd8  /go/pkg/mod/cache/download/github.com/!burnt!sushi/toml/@v/v1.6.0.zip' | sha256sum --check \
    && echo '4f5858c81cdef2d5cc07d764e491788e5965f631e3a955385471921dcc70ddf3  /go/pkg/mod/github.com/!burnt!sushi/toml@v1.6.0/parse.go' | sha256sum --check \
    && echo '8cfc6b34a572e0ea1c8c4d4422c57f2cb177e7c6a57099b62d2d69074a6e8a97  /go/pkg/mod/github.com/!burnt!sushi/toml@v1.6.0/lex.go' | sha256sum --check \
    && echo 'd21cb1c60785d6d3a84a7059323ccafc45c645b1bbda281c76a62d66ad2d7dc3  /go/pkg/mod/github.com/!burnt!sushi/toml@v1.6.0/COPYING' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/BurntSushi/toml -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
