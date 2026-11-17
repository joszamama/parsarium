#!/bin/sh
set -eu
if [ "${PARSARIUM_BUILD:-coverage}" = afl ]; then
    export CC=afl-clang-fast CXX=afl-clang-fast++
    export AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
else
    export CC=clang CXX=clang++
fi
PROFILE='-O1 -g -fprofile-instr-generate -fcoverage-mapping'
cmake -S /work/poppler-source -B /work/poppler-build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER="$CC" -DCMAKE_CXX_COMPILER="$CXX" \
  -DCMAKE_C_FLAGS="$PROFILE" -DCMAKE_CXX_FLAGS="$PROFILE" \
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
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
CFLAGS="$PROFILE" LDFLAGS='-fprofile-instr-generate' \
  meson setup /work/papers-build /work/papers-source \
  --prefix=/work/install --libdir=lib --buildtype=plain \
  -Dshell=false -Dpreviewer=false -Dthumbnailer=false -Dnautilus=false \
  -Dcomics=disabled -Ddjvu=disabled -Dpdf=enabled -Dtiff=disabled \
  -Dtests=false -Ddocumentation=false -Duser_doc=false -Dintrospection=disabled \
  -Dsysprof=disabled -Dkeyring=disabled -Dgtk_unix_print=disabled \
  -Dspell_check=disabled -Dfile_tests=false
meson compile -C /work/papers-build -j 4
meson install -C /work/papers-build --no-rebuild
test -f /work/install/lib/papers/6/backends/libpdfdocument.so
test -f /work/install/lib/libppsdocument-4.0.so
papers_flags=$(pkg-config --cflags --libs papers-document-4.0)
"$CC" -std=c11 -O1 -g -fno-omit-frame-pointer \
  -fprofile-instr-generate -fcoverage-mapping \
  /work/harness.c /work/replay.c $papers_flags -Wl,-rpath,/work/install/lib -o /work/replay
clang -std=c11 -O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer,address,undefined \
  /work/harness.c $papers_flags -Wl,-rpath,/work/install/lib -o /work/fuzzer
