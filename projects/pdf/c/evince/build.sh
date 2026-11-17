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

export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  LDFLAGS='-fprofile-instr-generate' \
  meson setup /work/evince-build /work/evince-source \
  --prefix=/work/install --libdir=lib --buildtype=plain \
  -Dviewer=false -Dpreviewer=false -Dthumbnailer=false \
  -Dcomics=disabled -Ddjvu=disabled -Ddvi=disabled -Dpdf=enabled \
  -Dps=disabled -Dtiff=disabled -Dxps=disabled \
  -Dgtk_doc=false -Duser_doc=false -Dintrospection=false \
  -Ddbus=false -Dkeyring=disabled -Dgtk_unix_print=disabled \
  -Dthumbnail_cache=disabled -Dmultimedia=disabled -Dgspell=disabled \
  -Dinternal_synctex=true -Dsystemduserunitdir=no
meson compile -C /work/evince-build -j 4
meson install -C /work/evince-build
test -f /work/install/lib/evince/4/backends/libpdfdocument.so
test -f /work/install/lib/libevdocument3.so

evince_flags=$(pkg-config --cflags --libs evince-document-3.0)
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping \
  /work/harness.c /work/replay.c $evince_flags -Wl,-rpath,/work/install/lib -o /work/replay
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer,address,undefined \
  /work/harness.c $evince_flags -Wl,-rpath,/work/install/lib -o /work/fuzzer
