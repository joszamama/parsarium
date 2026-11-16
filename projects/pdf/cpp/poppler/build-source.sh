#!/bin/sh
set -eu
# Poppler core plus the C++ frontend only. Rendering backends that are
# optional (Cairo, Boost Splash acceleration), UI frontends (GLib, Qt5, Qt6),
# command-line utilities, image codecs for JPX/DCT/TIFF/PNG, color
# management, network, signature backends, and font discovery are disabled.
# Splash and FreeType stay because Poppler core always compiles them.
cmake -S /work/source -B /work/build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_CXX_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_SHARED_LINKER_FLAGS='-fprofile-instr-generate' \
  -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib \
  -DBUILD_SHARED_LIBS=ON -DENABLE_CPP=ON -DFONT_CONFIGURATION=generic \
  -DENABLE_UTILS=OFF -DENABLE_GLIB=OFF -DENABLE_GOBJECT_INTROSPECTION=OFF -DENABLE_GTK_DOC=OFF \
  -DENABLE_QT5=OFF -DENABLE_QT6=OFF -DENABLE_BOOST=OFF -DWITH_Cairo=OFF -DWITH_PNG=OFF \
  -DENABLE_LIBOPENJPEG=OFF -DENABLE_LIBJPEG=OFF -DENABLE_LIBTIFF=OFF -DENABLE_LCMS=OFF \
  -DENABLE_LIBCURL=OFF -DENABLE_NSS3=OFF -DENABLE_GPGME=OFF -DENABLE_BROTLI=OFF -DENABLE_HARFBUZZ=OFF \
  -DBUILD_MANUAL_TESTS=OFF -DBUILD_CPP_TESTS=OFF -DBUILD_GTK_TESTS=OFF \
  -DBUILD_QT5_TESTS=OFF -DBUILD_QT6_TESTS=OFF -DRUN_GPERF_IF_PRESENT=OFF
cmake --build /work/build --parallel 6 --target poppler-cpp
cmake --install /work/build
