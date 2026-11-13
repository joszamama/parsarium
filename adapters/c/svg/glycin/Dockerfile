FROM ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    build-essential pkg-config libglib2.0-dev libseccomp-dev librsvg2-dev \
    libcairo2-dev meson ninja-build rustc cargo gettext libfontconfig1-dev \
    ca-certificates && rm -rf /var/lib/apt/lists/*

COPY glycin-2.2.6.tar.xz /tmp/glycin-2.2.6.tar.xz
RUN echo '6a114aa1117ec2d7bd578c8cefd235d993304dedfd1a62575dc31be9a146b791  /tmp/glycin-2.2.6.tar.xz' | sha256sum -c - && \
    mkdir /tmp/glycin-src && tar -xf /tmp/glycin-2.2.6.tar.xz -C /tmp/glycin-src && \
    meson setup /tmp/glycin-build /tmp/glycin-src/glycin-2.2.6 \
      --prefix=/usr/local -Dloaders=glycin-svg -Dglycin-loaders=true \
      -Dlibglycin=true -Dlibglycin-gtk4=false -Dglycin-thumbnailer=false \
      -Dtests=false -Dintrospection=false -Dvapi=false -Dprofile=release -Dlto=false && \
    meson compile -C /tmp/glycin-build -j4 && \
    meson install -C /tmp/glycin-build && ldconfig && \
    test "$(pkg-config --modversion glycin-2)" = '2.2.6'
