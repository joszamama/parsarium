FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/auxten/postgresql-parser \
    && echo '87ce5aa7debce0932a7758a2bbd8c1d2cd4efe5669f37db13ccfc84533a2e1ef  /go/pkg/mod/cache/download/github.com/auxten/postgresql-parser/@v/v1.0.1.zip' | sha256sum --check \
    && echo '8a2fba9d26592ff3538f44c96d1b894ef44649058b4d04f3fda49518a9c4ae11  /go/pkg/mod/github.com/auxten/postgresql-parser@v1.0.1/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
COPY replay/main.go ./replay/main.go
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/auxten/postgresql-parser/pkg/sql/parser -o /work/harness.test . \
    && CGO_ENABLED=0 go build -o /work/replay-bin ./replay
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/replay-bin /work/replay
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
