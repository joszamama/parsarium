FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-14-dev llvm make patch pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
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
RUN echo '54436603c4e8ccbc1b12c715b5e89bb03cbda448f3c3005c23d208109ccc19ed  /work/cgo-compat.patch' | sha256sum --check \
    && go mod download \
    && echo 'd2c93190df9ceca2a8769288997a917f0b08b6b03151e851972aba5d40250a3b  /go/pkg/mod/cache/download/github.com/moovweb/gokogiri/@v/v0.0.0-20180713195410-a1a828153468.zip' | sha256sum --check \
    && echo '04406b436ce743c0b446959df535268a454ab9da83e338cf87f18d667e9b70b4  /go/pkg/mod/github.com/moovweb/gokogiri@v0.0.0-20180713195410-a1a828153468/LICENSE' | sha256sum --check \
    && cp -a /go/pkg/mod/github.com/moovweb/gokogiri@v0.0.0-20180713195410-a1a828153468 /work/thirdparty \
    && chmod -R u+w /work/thirdparty \
    && cd /work/thirdparty && patch -p1 --fuzz=0 < /work/cgo-compat.patch \
    && printf 'module github.com/moovweb/gokogiri\n\ngo 1.27.1\n' > /work/thirdparty/go.mod
RUN go mod edit -replace github.com/moovweb/gokogiri=/work/thirdparty
ENV PKG_CONFIG_PATH=/opt/libxml2/lib/pkgconfig
ENV CC=clang
ENV CGO_ENABLED=1
ENV CGO_LDFLAGS=-fprofile-instr-generate
COPY harness.go harness_test.go native_profile.go native_profile_afl.go ./
COPY cmd/replay/main.go ./cmd/replay/main.go
COPY controls ./controls
COPY report.py ./
RUN go test -c -coverpkg=github.com/moovweb/gokogiri/xml -o /work/harness.test . \
    && go build -o /work/replay ./cmd/replay
ENTRYPOINT ["python3", "/work/report.py"]
