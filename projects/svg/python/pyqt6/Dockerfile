FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96 AS build
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    ca-certificates clang cmake curl libclang-rt-21-dev llvm ninja-build patchelf pkg-config python3 python3-venv \
    libfontconfig1-dev libfreetype-dev libpng-dev zlib1g-dev libpcre2-dev xz-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /work
RUN curl --fail --location --retry 3 --silent --show-error https://ftp.fau.de/qtproject/archive/qt/6.12/6.12.0/submodules/qtbase-everywhere-src-6.12.0.tar.xz -o /work/qtbase.tar.xz \
 && echo 'a951bd163c7b80fc6b8c88d7668fb56abf91c152373e13c10666763238131307  /work/qtbase.tar.xz' | sha256sum --check \
 && mkdir /work/qtbase && tar -xJf /work/qtbase.tar.xz -C /work/qtbase --strip-components=1
COPY build-qtbase.sh /work/
RUN chmod +x /work/build-qtbase.sh && /work/build-qtbase.sh && rm -rf /work/qtbase-build /work/qtbase /work/qtbase.tar.xz
RUN curl --fail --location --retry 3 --silent --show-error https://ftp.fau.de/qtproject/archive/qt/6.12/6.12.0/submodules/qtsvg-everywhere-src-6.12.0.tar.xz -o /work/source.tar.xz \
 && echo 'e4ab39534ec97987b1b9b60ef7f4d3253d5912a69f8c713a01753174a4029331  /work/source.tar.xz' | sha256sum --check \
 && mkdir /work/source && tar -xJf /work/source.tar.xz -C /work/source --strip-components=1
COPY build-qtsvg.sh /work/
RUN chmod +x /work/build-qtsvg.sh && /work/build-qtsvg.sh
RUN mkdir /work/wheels \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/37/5e/5154ead9550aed78ecf9adddb2d5087ac8878cb9c337834b951c32763fae/pyqt6-6.12.0-cp310-abi3-manylinux_2_39_aarch64.whl --output /work/wheels/pyqt6-6.12.0-cp310-abi3-manylinux_2_39_aarch64.whl \
    && echo '2799f2e75594af313222a2dc2da9f965fe88be29ee4293d7937e7763630f5610  /work/wheels/pyqt6-6.12.0-cp310-abi3-manylinux_2_39_aarch64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/62/85/4987f605abd8854eaaefe7a26e5926bab0600985984aa5555cf0d8d7cb2f/pyqt6_qt6-6.12.0-py3-none-manylinux_2_39_aarch64.whl --output /work/wheels/pyqt6_qt6-6.12.0-py3-none-manylinux_2_39_aarch64.whl \
    && echo '2460119ac5f725cfddc331bd56eca22fbb61b29a549d417b7bcc304c7fc9459b  /work/wheels/pyqt6_qt6-6.12.0-py3-none-manylinux_2_39_aarch64.whl' | sha256sum --check \
    && curl --fail --location --retry 3 https://files.pythonhosted.org/packages/5e/d1/95c6481ab4017cd4c3d50bc34401b6ae24aeade473426cc501692ff62180/pyqt6_sip-13.13.1-cp314-cp314-manylinux_2_17_aarch64.manylinux2014_aarch64.whl --output /work/wheels/pyqt6_sip-13.13.1-cp314-cp314-manylinux_2_17_aarch64.manylinux2014_aarch64.whl \
    && echo '4a751c542ffb7afcc945eb824fc3fa3c3dae002c91fe5c1da86a5a567c6271b9  /work/wheels/pyqt6_sip-13.13.1-cp314-cp314-manylinux_2_17_aarch64.manylinux2014_aarch64.whl' | sha256sum --check \
    && python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-index --no-deps /work/wheels/*.whl
# Swap only the wheel's prebuilt QtSvg library for the same 6.12.0 release built from
# source with LLVM coverage; the PyQt6 binding and the wheel's QtCore/QtGui stay pinned.
RUN lib=/opt/venv/lib/python3.14/site-packages/PyQt6/Qt6/lib \
    && sha256sum $lib/libQt6Svg.so.6 > /work/wheel-qtsvg.sha256 \
    && cp "$(readlink -f /work/qt/lib/libQt6Svg.so.6)" $lib/libQt6Svg.so.6 \
    && patchelf --set-rpath '$ORIGIN' $lib/libQt6Svg.so.6 \
    && { python3 --version; /opt/venv/bin/pip show PyQt6 PyQt6-Qt6 | grep -E '^(Name|Version):'; \
         clang --version | head -1; llvm-cov --version | head -1; \
         echo "replaced wheel QtSvg $(cut -d' ' -f1 /work/wheel-qtsvg.sha256)"; \
         sha256sum $lib/libQt6Svg.so.6 /work/source/src/svg/qsvghandler.cpp; } > /work/toolchain.txt

FROM --platform=linux/arm64 ubuntu@sha256:065aa8626841f16057b78b027b464cd59c4fac36c204c72dcbf48d66f5fa8a96
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    llvm libstdc++6 python3 libdbus-1-3 libglib2.0-0 libgl1 libegl1 libxkbcommon0 libfreetype6 libfontconfig1 \
    libx11-6 libxcb1 libxrender1 libxext6 libsm6 libice6 \
    && rm -rf /var/lib/apt/lists/*
ENV QT_HASH_SEED=0
ENV QT_QPA_PLATFORM=offscreen
ENV LLVM_PROFILE_FILE=/tmp/parsarium-qtsvg-%p.profraw
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /work
COPY --from=build /opt/venv /opt/venv
COPY --from=build /work/source/src/svg /work/source/src/svg
COPY --from=build /work/toolchain.txt /work/toolchain.txt
COPY harness.py fuzz.py run-control.py target.json /work/
ENTRYPOINT ["/opt/venv/bin/python", "/work/run-control.py"]
