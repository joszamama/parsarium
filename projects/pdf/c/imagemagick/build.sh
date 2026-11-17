#!/bin/sh
set -eu
# Both parser builds stay in build.sh so the AFL++ overlay's compiler rewrite
# instruments ImageMagick and the Ghostscript library it calls in process.
cd /work/ghostscript
# ImageMagick decodes Ghostscript's PNG page output with its own PNG coder.
# Drop the bundled libpng and zlib so libgs and ImageMagick share one system
# copy instead of exporting two libpng symbol sets into the same process.
rm -rf libpng zlib
./configure CC=clang --without-x --disable-gtk --disable-cups --disable-dbus --disable-fontconfig \
  --without-tesseract --without-libpaper --without-libidn --without-ijs --without-local-zlib \
  --without-pcl --without-xps --without-gpdl --with-drivers=FILES
make -j 6 so-only XCFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' XLDFLAGS='-fprofile-instr-generate'
# The headers that Ghostscript's soinstall target places under include/ghostscript.
mkdir -p /work/gs-include/ghostscript
cp psi/iapi.h psi/ierrors.h base/gserrors.h /work/gs-include/ghostscript/
# --with-gslib defines MAGICKCORE_GS_DELEGATE, so coders/ghostscript-private.h
# calls gsapi_* in process. No gs executable exists here, so configure keeps the
# default png16malpha alpha device that libgs provides through FILES.
cd /work/source
LD_LIBRARY_PATH=/work/ghostscript/sobin ./configure CC=clang \
  CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
  CPPFLAGS='-I/work/gs-include' LDFLAGS='-fprofile-instr-generate -L/work/ghostscript/sobin' \
  --prefix=/work/install --disable-shared --enable-static --disable-openmp \
  --without-modules --without-utilities --without-x --without-perl --without-magick-plus-plus \
  --with-gslib=yes --with-png=yes --with-zlib=yes \
  --without-bzlib --without-djvu --without-fontconfig --without-freetype --without-raqm \
  --without-heic --without-jbig --without-jpeg --without-jxl --without-lcms --without-openjp2 \
  --without-lqr --without-lzma --without-openexr --without-pango --without-raw --without-tiff \
  --without-webp --without-xml --without-zip --without-zstd
grep -Eq '^#define MAGICKCORE_GS_DELEGATE +1' MagickCore/magick-baseconfig.h
LD_LIBRARY_PATH=/work/ghostscript/sobin make -j 4
make install
cd /work
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
im_cflags=$(pkg-config --cflags MagickWand)
im_libs="$(pkg-config --static --libs MagickWand) -L/work/ghostscript/sobin -lgs -Wl,-rpath,/work/lib"
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping $im_cflags /work/harness.c /work/replay.c $im_libs -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -fprofile-instr-generate $im_cflags /work/harness.c $im_libs -o /work/fuzzer
