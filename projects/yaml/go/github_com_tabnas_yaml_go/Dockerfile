FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/tabnas/yaml/go github.com/tabnas/jsonic/go github.com/tabnas/parser/go github.com/tabnas/json/go \
    && echo 'ffd7e147ac3a91ce4401fbea0542c6984cba345041c1b004d02ec08efd0b84ae  /go/pkg/mod/cache/download/github.com/tabnas/yaml/go/@v/v0.5.32.zip' | sha256sum --check \
    && echo '977949d02b883c911222908c131433288a426b23a0a6d2bba1064d489b9fce9d  /go/pkg/mod/cache/download/github.com/tabnas/jsonic/go/@v/v0.7.11.zip' | sha256sum --check \
    && echo '7e8c98a38bb9d3c67f76c86fc1e9468bb7facf1a4b66198891bafa9c9595147b  /go/pkg/mod/cache/download/github.com/tabnas/parser/go/@v/v0.12.20.zip' | sha256sum --check \
    && echo '0f4bc618a9d15f64e5e62ab8118d518c39c64fe5cd0871109d4b1962b7e330b4  /go/pkg/mod/cache/download/github.com/tabnas/json/go/@v/v0.5.20.zip' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/tabnas/yaml/go,github.com/tabnas/jsonic/go,github.com/tabnas/parser/go,github.com/tabnas/json/go -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
