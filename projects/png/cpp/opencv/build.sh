#!/bin/sh
set -eu

# One static build of the modules imread needs for PNG: imgcodecs -> imgproc ->
# geometry -> flann -> core. libpng and zlib come from the pinned OpenCV
# tarball's 3rdparty tree, so their source is covered by the same checksum.
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
cmake -S /work/source -B /work/opencv-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib \
  -DBUILD_SHARED_LIBS=OFF -DBUILD_LIST=core,flann,geometry,imgproc,imgcodecs \
  -DOPENCV_FORCE_3RDPARTY_BUILD=OFF -DBUILD_ZLIB=ON -DWITH_ZLIB_NG=OFF \
  -DWITH_PNG=ON -DBUILD_PNG=ON -DWITH_SPNG=OFF -DPNG_ARM_NEON=off \
  -DWITH_JPEG=OFF -DWITH_TIFF=OFF -DWITH_WEBP=OFF -DWITH_OPENJPEG=OFF -DWITH_JASPER=OFF \
  -DWITH_OPENEXR=OFF -DWITH_AVIF=OFF -DWITH_JPEGXL=OFF -DWITH_GDAL=OFF -DWITH_GDCM=OFF \
  -DWITH_IMGCODEC_GIF=OFF -DWITH_IMGCODEC_HDR=OFF -DWITH_IMGCODEC_SUNRASTER=OFF \
  -DWITH_IMGCODEC_PXM=OFF -DWITH_IMGCODEC_PFM=OFF \
  -DWITH_IPP=OFF -DWITH_ITT=OFF -DWITH_OPENCL=OFF \
  -DWITH_OPENCLAMDFFT=OFF -DWITH_OPENCLAMDBLAS=OFF \
  -DWITH_EIGEN=OFF -DWITH_LAPACK=OFF \
  -DWITH_KLEIDICV=OFF -DWITH_CAROTENE=OFF -DWITH_FASTCV=OFF -DWITH_TBB=OFF -DWITH_OPENMP=OFF \
  -DWITH_HARFBUZZ=OFF -DWITH_PROTOBUF=OFF -DWITH_FLATBUFFERS=OFF -DWITH_OBSENSOR=OFF \
  -DWITH_GTK=OFF -DWITH_QT=OFF -DWITH_VTK=OFF -DWITH_FFMPEG=OFF -DWITH_GSTREAMER=OFF \
  -DWITH_V4L=OFF -DWITH_VA=OFF -DWITH_VA_INTEL=OFF -DWITH_CUDA=OFF \
  -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DBUILD_EXAMPLES=OFF -DBUILD_DOCS=OFF \
  -DBUILD_opencv_apps=OFF -DBUILD_JAVA=OFF -DBUILD_opencv_python3=OFF \
  -DENABLE_CCACHE=OFF -DENABLE_PRECOMPILED_HEADERS=OFF -DENABLE_OMIT_FRAME_POINTER=OFF \
  -DENABLE_CONFIG_VERIFICATION=ON
cmake --build /work/opencv-build -j 4
cmake --install /work/opencv-build

lib=/work/install/lib
third=/work/install/lib/opencv5/3rdparty
libs="$lib/libopencv_imgcodecs.a $lib/libopencv_imgproc.a $lib/libopencv_geometry.a $lib/libopencv_flann.a $lib/libopencv_core.a $third/liblibpng.a $third/libzlib.a"
for archive in $libs; do test -f "$archive"; done

clang++ -std=c++17 $common -I/work/install/include/opencv5 -c /work/harness.cpp -o /work/harness.o
clang++ -std=c++17 $common -c /work/replay.cpp -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping -fsanitize=address,undefined \
  /work/harness.o /work/replay.o $libs -ldl -lpthread -o /work/replay
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer,address,undefined \
  /work/harness.o $libs -ldl -lpthread -o /work/fuzzer
