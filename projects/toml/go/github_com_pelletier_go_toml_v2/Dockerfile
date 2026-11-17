FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'bc0de16d4942df8503be13bde0447e0b7ce1694f3bb1b840f485ce839f8974cf  /go/pkg/mod/cache/download/github.com/pelletier/go-toml/v2/@v/v2.4.3.zip' | sha256sum --check \
    && echo '4c95165b69f4cb942140164abf3e060c5df4d43eb7e79b08c253d707f3798b25  /go/pkg/mod/github.com/pelletier/go-toml/v2@v2.4.3/unstable/parser.go' | sha256sum --check \
    && echo '26844e4b53c5adec04e557fd7dfef281cc0205a7d355626b1c68b778b99e9e7b  /go/pkg/mod/github.com/pelletier/go-toml/v2@v2.4.3/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/pelletier/go-toml/v2/... -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
