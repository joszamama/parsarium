#!/bin/sh
set -eu
# Both parser builds stay in build.sh so the AFL++ overlay's compiler rewrite
# instruments ImageMagick and the Ghostscript library it calls in process.
cd /work/ghostscript
./configure CC=clang --without-x --disable-gtk --disable-cups --disable-dbus --disable-fontconfig \
  --without-tesseract --without-libpaper --without-libidn --without-ijs \
  --without-pcl --without-xps --without-gpdl --with-drivers=FILES
make -j 6 so-only XCFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' XLDFLAGS='-fprofile-instr-generate'
# The headers that Ghostscript's soinstall target places under include/ghostscript.
mkdir -p /work/gs-include/ghostscript
cp psi/iapi.h psi/ierrors.h base/gserrors.h /work/gs-include/ghostscript/
# Upstream --with-gslib defines MAGICKCORE_GS_DELEGATE; the PDF coder then
# calls gsapi_* from coders/ghostscript-private.h instead of running gs.
export LD_LIBRARY_PATH=/work/ghostscript/sobin
cd /work/source
CC=clang CXX=clang++ CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 CPPFLAGS='-I/work/gs-include' LDFLAGS='-fprofile-instr-generate -L/work/ghostscript/sobin' \
 ./configure --prefix=/work/install --disable-shared --enable-static --disable-openmp --disable-docs \
 --without-x --with-magick-plus-plus --without-modules --without-utilities --without-perl \
 --with-gslib=yes --with-png=yes --with-zlib=yes \
 --without-bzlib --without-djvu --without-dps --without-fftw --without-flif --without-fpx \
 --without-fontconfig --without-freetype --without-gvc --without-heic --without-jbig --without-jpeg \
 --without-jxl --without-lcms --without-lqr --without-lzma --without-openexr --without-openjp2 \
 --without-pango --without-raqm --without-raw --without-rsvg --without-tiff --without-uhdr \
 --without-webp --without-wmf --without-xml --without-zip --without-zstd
make -j 4
make install
grep -q '^#define MAGICKCORE_GS_DELEGATE 1' /work/install/include/ImageMagick-7/MagickCore/magick-baseconfig.h
cd /work
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
im_cflags=$(pkg-config --cflags Magick++)
im_libs="$(pkg-config --static --libs Magick++) -L/work/ghostscript/sobin -lgs -Wl,-rpath,/work/lib"
common='-std=c++17 -O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $im_cflags /work/harness.cpp /work/replay.cpp $im_libs -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined -fprofile-instr-generate $im_cflags /work/harness.cpp $im_libs -o /work/fuzzer
