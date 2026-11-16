#!/bin/sh
set -eu
# PoDoFo library only. Font discovery (fontconfig), AFDKO CFF subsetting,
# ICC color management, and JPEG/TIFF/PNG image codecs are disabled; none is
# on the PdfMemDocument load and page-count path. OpenSSL, FreeType, libxml2,
# and zlib remain because PoDoFo's CMake requires them unconditionally.
cmake -S /work/source -B /work/build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_CXX_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_SHARED_LINKER_FLAGS='-fprofile-instr-generate' \
  -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib \
  -DPODOFO_BUILD_LIB_ONLY=ON -DPODOFO_BUILD_STATIC=OFF \
  -DPODOFO_WITH_FONTMANAGER=OFF -DPODOFO_WITH_AFDKO=OFF -DPODOFO_WITH_LCMS2=OFF \
  -DCMAKE_DISABLE_FIND_PACKAGE_JPEG=ON -DCMAKE_DISABLE_FIND_PACKAGE_TIFF=ON \
  -DCMAKE_DISABLE_FIND_PACKAGE_PNG=ON -DCMAKE_DISABLE_FIND_PACKAGE_Doxygen=ON
cmake --build /work/build --parallel 6 --target podofo_shared
cmake --install /work/build
