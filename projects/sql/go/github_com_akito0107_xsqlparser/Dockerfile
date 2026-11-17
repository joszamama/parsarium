FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/akito0107/xsqlparser \
    && echo 'e7e6f22ab8304c399adefdfcb5a6b80c7677c10f69c0159b25903c73e8109f3c  /go/pkg/mod/cache/download/github.com/akito0107/xsqlparser/@v/v1.0.0.zip' | sha256sum --check \
    && echo 'e3c54bff28da2bcc5214064c0d4da3cb976f9c4ebdae9da9ae6976cfd01c34e9  /go/pkg/mod/github.com/akito0107/xsqlparser@v1.0.0/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
COPY replay/main.go ./replay/main.go
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/akito0107/xsqlparser,github.com/akito0107/xsqlparser/sqltoken -o /work/harness.test . \
    && CGO_ENABLED=0 go build -o /work/replay-bin ./replay
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/replay-bin /work/replay
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
