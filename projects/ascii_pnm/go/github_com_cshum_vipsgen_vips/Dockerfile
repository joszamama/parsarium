FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-14-dev libexpat1-dev libglib2.0-dev llvm make \
    meson ninja-build pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://github.com/libvips/libvips/releases/download/v8.18.7/vips-8.18.7.tar.xz -o /work/vips.tar.xz \
    && echo '5baaead3b0bb20ffdb9e9ff09aa9fda08620923df77b63b436654cb5e0b3bf94  /work/vips.tar.xz' | sha256sum --check \
    && mkdir /work/vips-source && tar -xJf /work/vips.tar.xz -C /work/vips-source --strip-components=1
ENV VIPS_MESON="--prefix=/opt/vips --libdir=lib --default-library=static --buildtype=plain \
    --auto-features=disabled -Dcplusplus=false -Dexamples=false -Ddocs=false -Dcpp-docs=false \
    -Dvapi=false -Dppm=true"
ENV VIPS_PC_FIX="s/^Requires.private:/Requires:/; s/^Libs: \\(.*\\)$/Libs: \\1 -lstdc++ -lm -lpthread/"
RUN cd /work/vips-source \
    && CC=clang CXX=clang++ CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' meson setup build $VIPS_MESON \
    && ninja -C build && ninja -C build install \
    && sed -i "$VIPS_PC_FIX" /opt/vips/lib/pkgconfig/vips.pc
COPY go.mod go.sum ./
RUN go mod download \
    && echo '579ca148c80ec89469257e0df8c78a47cbc2cfc895ef09f7fa0933fbd1749dcf  /go/pkg/mod/cache/download/github.com/cshum/vipsgen/@v/v1.3.11.zip' | sha256sum --check \
    && echo 'b64d87ab949b954be3d25e089d03fba81c6556c73dec44af6d79e48afd506a71  /go/pkg/mod/github.com/cshum/vipsgen@v1.3.11/LICENSE' | sha256sum --check
ENV PKG_CONFIG_PATH=/opt/vips/lib/pkgconfig
ENV CC=clang
ENV CGO_ENABLED=1
ENV CGO_LDFLAGS=-fprofile-instr-generate
COPY harness.go harness_test.go native_profile.go native_profile_afl.go ./
COPY cmd/replay/main.go ./cmd/replay/main.go
COPY controls ./controls
COPY report.py ./
RUN go test -c -coverpkg=github.com/cshum/vipsgen/vips -o /work/harness.test . \
    && go build -o /work/replay ./cmd/replay
ENTRYPOINT ["python3", "/work/report.py"]
