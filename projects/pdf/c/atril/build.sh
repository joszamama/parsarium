#!/bin/sh
set -eu

# Build Poppler's GLib frontend and PDF core from the pinned source archive.
cmake -S /work/source -B /work/poppler-build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_CXX_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_SHARED_LINKER_FLAGS='-fprofile-instr-generate' \
  -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib \
  -DBUILD_SHARED_LIBS=ON -DENABLE_GLIB=ON -DWITH_Cairo=ON -DWITH_GLIB=ON -DWITH_GTK=OFF \
  -DENABLE_CPP=OFF -DFONT_CONFIGURATION=generic \
  -DENABLE_UTILS=OFF -DENABLE_GOBJECT_INTROSPECTION=OFF -DENABLE_GTK_DOC=OFF \
  -DENABLE_QT5=OFF -DENABLE_QT6=OFF -DENABLE_BOOST=OFF -DWITH_PNG=OFF \
  -DENABLE_LIBOPENJPEG=OFF -DENABLE_LIBJPEG=OFF -DENABLE_LIBTIFF=OFF -DENABLE_LCMS=OFF \
  -DENABLE_LIBCURL=OFF -DENABLE_NSS3=OFF -DENABLE_GPGME=OFF -DENABLE_BROTLI=OFF -DENABLE_HARFBUZZ=OFF \
  -DBUILD_MANUAL_TESTS=OFF -DBUILD_CPP_TESTS=OFF -DBUILD_GTK_TESTS=OFF \
  -DBUILD_QT5_TESTS=OFF -DBUILD_QT6_TESTS=OFF -DRUN_GPERF_IF_PRESENT=OFF
cmake --build /work/poppler-build --parallel 5 --target poppler-glib
cmake --install /work/poppler-build
test -f /work/install/lib/libpoppler-glib.so

# Atril's release tarball ships a generated configure script. Only libdocument
# and the PDF backend are built; the viewer shell is configured but not compiled.
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
cd /work/atril-source
CC=clang CXX=clang++ \
  CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  CXXFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  LDFLAGS='' \
  ./configure --prefix=/work/install --libdir=/work/install/lib \
  --disable-static --disable-maintainer-mode --disable-dependency-tracking \
  --disable-nls --disable-dbus --disable-caja --disable-thumbnailer --disable-previewer \
  --disable-introspection --disable-synctex --disable-schemas-compile --disable-tests \
  --disable-ps --disable-tiff --disable-djvu --disable-dvi \
  --without-keyring --without-gtk-unix-print
make -C libdocument -j 4
make -C libdocument install
make -C backend -j 4
make -C backend install
make install-headerDATA install-pkgconfigDATA
test -f /work/install/lib/atril/3/backends/libpdfdocument.so
test -f /work/install/lib/atril/3/backends/pdfdocument.atril-backend
test -f /work/install/lib/libatrildocument.so

atril_flags=$(pkg-config --cflags --libs atril-document-1.5.0)
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping \
  /work/harness.c /work/replay.c $atril_flags -Wl,--export-dynamic -Wl,-rpath,/work/install/lib -o /work/replay
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer,address,undefined \
  /work/harness.c $atril_flags -Wl,--export-dynamic -Wl,-rpath,/work/install/lib -o /work/fuzzer
