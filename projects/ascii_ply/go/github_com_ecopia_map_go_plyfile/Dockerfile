FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'e4354ba6d72c6743455d62fbde8e6b47e54cb255cda8811c6053c3b6fb761df4  /go/pkg/mod/cache/download/github.com/ecopia-map/go-plyfile/@v/v1.0.0.zip' | sha256sum --check
RUN cd /go/pkg/mod/github.com/ecopia-map/go-plyfile@v1.0.0/lib && make all \
    && python3 -c 'from pathlib import Path; p=Path("/go/pkg/mod/github.com/ecopia-map/go-plyfile@v1.0.0/plyfile.go");s=p.read_text();old="/*\n#include <string.h>\n#include \"lib/ply.h\"";assert s.count(old)==1;p.write_text(s.replace(old,"/*\n#cgo LDFLAGS: -L${SRCDIR}/lib -lplyfile\n#include <string.h>\n#include \"lib/ply.h\""))' \
    && echo 'd32b09a4edae6c8192aca03830a06373240a91619bc3f329c0c2fcbae6dee79f  /go/pkg/mod/github.com/ecopia-map/go-plyfile@v1.0.0/plyfile.go' | sha256sum --check
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=1 go test -c -coverpkg=github.com/ecopia-map/go-plyfile -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
