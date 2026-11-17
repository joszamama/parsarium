FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang curl libclang-rt-14-dev llvm make pkg-config xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 https://downloads.sourceforge.net/project/graphicsmagick/graphicsmagick/1.3.49/GraphicsMagick-1.3.49.tar.xz -o /work/gm.tar.xz \
    && echo '7efa070dc31116b4315061b39f84bc7181e8b060bf61214ec9af851131af9c81  /work/gm.tar.xz' | sha256sum --check \
    && mkdir /work/gm-source && tar -xJf /work/gm.tar.xz -C /work/gm-source --strip-components=1
ENV GM_CONFIGURE="--prefix=/opt/gm --disable-shared --enable-static --disable-openmp \
    --without-magick-plus-plus --without-perl --without-x --without-bzlib --without-zlib \
    --without-zstd --without-lzma --without-jpeg --without-jbig --without-jp2 --without-png \
    --without-tiff --without-webp --without-wmf --without-xml --without-lcms2 --without-ttf \
    --without-gs --without-trio --without-dps --without-fpx --without-jxl --without-heif \
    --without-modules"
RUN cd /work/gm-source \
    && CC=clang CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
       LDFLAGS='-fprofile-instr-generate' ./configure $GM_CONFIGURE \
    && make -j4 && make install \
    && sed -i 's/^Libs: \(.*\)$/Libs: \1 -lm -lpthread/' /opt/gm/lib/pkgconfig/GraphicsMagick.pc /opt/gm/lib/pkgconfig/GraphicsMagickWand.pc
COPY go.mod go.sum ./
RUN go mod download \
    && echo '6efd2688d5323783ce893fa183a20ef76fdf4e548bc1e611f66119552431e4fe  /go/pkg/mod/cache/download/github.com/gographics/gmagick/@v/v1.0.0.zip' | sha256sum --check \
    && echo '134c7bac9cfff38c6fe91811c6f518de2bf7881befe6b1b737ba8310da09b226  /go/pkg/mod/github.com/gographics/gmagick@v1.0.0/LICENSE' | sha256sum --check
ENV PKG_CONFIG_PATH=/opt/gm/lib/pkgconfig
ENV CC=clang
ENV CGO_ENABLED=1
ENV CGO_LDFLAGS=-fprofile-instr-generate
COPY harness.go harness_test.go native_profile.go native_profile_afl.go ./
COPY cmd/replay/main.go ./cmd/replay/main.go
COPY controls ./controls
COPY report.py ./
RUN go test -c -coverpkg=github.com/gographics/gmagick -o /work/harness.test . \
    && go build -o /work/replay ./cmd/replay
ENTRYPOINT ["python3", "/work/report.py"]
