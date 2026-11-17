FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    clang=1:14.0-55.7~deb12u1 llvm=1:14.0-55.7~deb12u1 \
    libclang-rt-14-dev=1:14.0.6-12 python3 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo '1b22cd1e7df4e1ea0ef7c4a41c899430dbf42f13e2cfe2c771d27b56809c87e8  /go/pkg/mod/cache/download/github.com/tosone/minimp3/@v/v1.1.0.zip' | sha256sum --check
COPY adapter.go harness_test.go native_profile.go report.py ./
RUN CC=clang CGO_ENABLED=1 CGO_CFLAGS='-fprofile-instr-generate -fcoverage-mapping' \
    CGO_LDFLAGS='-fprofile-instr-generate' \
    go test -c -coverpkg=github.com/tosone/minimp3 -o /work/harness.test .
ENTRYPOINT ["python3", "/work/report.py"]
