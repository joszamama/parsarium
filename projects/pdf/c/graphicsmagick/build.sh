#!/bin/sh
set -eu
# Both parser builds stay in build.sh so the AFL++ overlay's compiler rewrite
# instruments GraphicsMagick and the Ghostscript library it calls in process.
cd /work/ghostscript
./configure CC=clang --without-x --disable-gtk --disable-cups --disable-dbus --disable-fontconfig \
  --without-tesseract --without-libpaper --without-libidn --without-ijs \
  --without-pcl --without-xps --without-gpdl --with-drivers=FILES
make -j 6 so-only XCFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' XLDFLAGS='-fprofile-instr-generate'
# The headers that Ghostscript's soinstall target places under include/ghostscript.
mkdir -p /work/gs-include/ghostscript
cp psi/iapi.h psi/ierrors.h base/gserrors.h /work/gs-include/ghostscript/
# Configure removed --with-gslib in 1.3.31; upstream keeps the in-process
# delegate behind HasGSLIB and documents enabling it through CPPFLAGS and LIBS.
# GraphicsMagick 1.3.49 declares gs_main_instance* where Ghostscript 10 uses
# void*; the C compiler must accept that ABI-identical function-pointer mismatch.
cd /work/source
LD_LIBRARY_PATH=/work/ghostscript/sobin ./configure CC=clang \
  CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -Wno-incompatible-function-pointer-types' \
  CPPFLAGS='-DHasGSLIB -I/work/gs-include' \
  LDFLAGS='-fprofile-instr-generate -L/work/ghostscript/sobin' LIBS='-lgs' \
  --prefix=/work/install --disable-shared --enable-static --enable-symbol-prefix --disable-openmp \
  --without-modules --without-x --without-perl --without-magick-plus-plus --without-bzlib \
  --without-jbig --without-webp --without-heif --without-jpeg --without-jp2 --without-jxl \
  --without-lcms2 --without-lzma --without-png --without-tiff --without-ttf --without-libzip \
  --without-wmf --without-xml --without-zlib --without-zstd
LD_LIBRARY_PATH=/work/ghostscript/sobin make -j 6
make install
cd /work
export PATH=/work/install/bin:$PATH
gm_cflags=$(/work/install/bin/GraphicsMagickWand-config --cppflags)
gm_libs="$(/work/install/bin/GraphicsMagickWand-config --ldflags --libs) -lgs -Wl,-rpath,/work/lib"
common='-O1 -g -fno-omit-frame-pointer'
clang $common -fprofile-instr-generate -fcoverage-mapping $gm_cflags /work/harness.c /work/replay.c $gm_libs -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined -fprofile-instr-generate $gm_cflags /work/harness.c $gm_libs -o /work/fuzzer
