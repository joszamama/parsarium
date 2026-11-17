FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-14-dev llvm make patch pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
# Same libxml2 2.15.4 source pin and configure flags as projects/xml/go/github_com_moovweb_gokogiri.
RUN curl --fail --location --retry 3 https://download.gnome.org/sources/libxml2/2.15/libxml2-2.15.4.tar.xz -o /work/libxml2.tar.xz \
    && echo '98087fd181d9070724f3fbc65c7377db03038eb92bd882374daff44940138821  /work/libxml2.tar.xz' | sha256sum --check \
    && mkdir /work/libxml2-source && tar -xJf /work/libxml2.tar.xz -C /work/libxml2-source --strip-components=1
RUN cd /work/libxml2-source \
    && CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' ./configure --prefix=/opt/libxml2 \
       --disable-shared --enable-static --without-python --without-zlib --without-lzma \
       --without-iconv --without-icu --without-http --without-modules --without-catalog \
    && make -j4 && make install
COPY go.mod go.sum cgo-compat.patch ./
# The pinned module predates libxml2 2.13+ prototypes (xmlNode ** instead of xmlNodePtr *);
# cgo-compat.patch changes one local variable type in clib.go so the binding compiles against 2.15.4.
RUN echo '73e32eecb64bdc702c0b1fc37dab0132bfe6a63ac2b444147b354f427f377fba  /work/cgo-compat.patch' | sha256sum --check \
    && go mod download \
    && echo '06853797762a758857acdd814eb3e634f93664d5439cfe15fc124562ab0a12ee  /go/pkg/mod/cache/download/github.com/lestrrat-go/libxml2/@v/v0.0.0-20260709020957-3f0f7bd60b63.zip' | sha256sum --check \
    && echo '0c4868a07b1c2dbb67c75767b4f1b2936c392d02ca2c7ee9827cac1a9d60ab1d  /go/pkg/mod/github.com/lestrrat-go/libxml2@v0.0.0-20260709020957-3f0f7bd60b63/LICENSE' | sha256sum --check \
    && echo '06a43ac87a173f390250fc01f098b45a1889b3a073c78c65a551ccc8c7e7b878  /go/pkg/mod/github.com/lestrrat-go/libxml2@v0.0.0-20260709020957-3f0f7bd60b63/clib/clib.go' | sha256sum --check \
    && cp -a /go/pkg/mod/github.com/lestrrat-go/libxml2@v0.0.0-20260709020957-3f0f7bd60b63 /work/thirdparty \
    && chmod -R u+w /work/thirdparty \
    && cd /work/thirdparty && patch -p1 --fuzz=0 < /work/cgo-compat.patch
RUN go mod edit -replace github.com/lestrrat-go/libxml2=/work/thirdparty
ENV PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig
ENV CC=clang
ENV CGO_ENABLED=1
ENV CGO_LDFLAGS='-fprofile-instr-generate -lm'
COPY harness.go harness_test.go native_profile.go native_profile_afl.go ./
COPY cmd/replay/main.go ./cmd/replay/main.go
COPY cmd/parse-only/main.go ./cmd/parse-only/main.go
COPY controls ./controls
COPY report.py ./
RUN go test -c -coverpkg=github.com/lestrrat-go/libxml2/... -o /work/harness.test . \
    && go build -o /work/replay ./cmd/replay
ENTRYPOINT ["python3", "/work/report.py"]
