FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
RUN apt-get update -qq && apt-get install -y --no-install-recommends libassimp-dev zlib1g-dev pkg-config && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download \
    && echo 'a9e502597d58103ab75477dfc31aade89f2e4e46ef26322fceb16730a699bfce  /go/pkg/mod/cache/download/github.com/andrebq/assimp/@v/v0.0.0-20121130215243-a775ba6866d8.zip' | sha256sum --check \
    && grep -q 'Permission is hereby granted' /go/pkg/mod/github.com/andrebq/assimp@v0.0.0-20121130215243-a775ba6866d8/LICENSE
COPY adapter.go harness_test.go ./
RUN CGO_ENABLED=1 go test -c -coverpkg=github.com/andrebq/assimp/conv,github.com/andrebq/assimp -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter

FROM --platform=linux/arm64 debian@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc
RUN apt-get update -qq && apt-get install -y --no-install-recommends libassimp5 && rm -rf /var/lib/apt/lists/*
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
