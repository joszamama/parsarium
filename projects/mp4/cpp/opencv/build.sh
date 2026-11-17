#!/bin/sh
set -eu

# FFmpeg and OpenCV share one instrumentation set, so coverage, libFuzzer and
# the AFL++ overlay (which rewrites the compilers below) all observe the FFmpeg
# MOV/MP4 demuxer, not only the OpenCV wrapper.
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined -fno-sanitize=function'

# FFmpeg 9.0.2 from its pinned release tarball. VideoCapture on a local MP4
# needs the file protocol, the mov demuxer and the H.264 decoder; the AAC
# decoder and parsers keep stream probing close to the catalog build.
# OpenCV's FFmpeg backend requires libswscale. Threads are off so decoding is
# single-threaded and deterministic; zlib serves compressed moov boxes.
cd /work/ffmpeg
./configure --prefix=/work/ffmpeg-install --cc=clang --cxx=clang++ \
  --disable-everything --disable-autodetect --disable-programs --disable-doc \
  --disable-network --disable-asm --disable-pthreads --disable-avdevice --disable-avfilter \
  --disable-swresample --disable-shared --enable-static --enable-zlib \
  --enable-protocol=file --enable-demuxer=mov \
  --enable-decoder=h264,aac --enable-parser=h264,aac \
  --extra-cflags="$common" --extra-cxxflags="$common" --extra-ldflags="$common"
make -j 4
make install

# One static build of the modules VideoCapture needs: videoio -> imgcodecs ->
# imgproc -> geometry -> flann -> core. FFmpeg is the only videoio backend;
# plugins, cameras and every image codec are off. The link test is skipped
# because pkg-config does not list the static FFmpeg archives' dependencies.
export PKG_CONFIG_PATH=/work/ffmpeg-install/lib/pkgconfig
cmake -S /work/source -B /work/opencv-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DCMAKE_INSTALL_PREFIX=/work/install -DCMAKE_INSTALL_LIBDIR=lib \
  -DBUILD_SHARED_LIBS=OFF -DBUILD_LIST=core,flann,geometry,imgproc,imgcodecs,videoio \
  -DWITH_FFMPEG=ON -DOPENCV_FFMPEG_SKIP_BUILD_CHECK=ON -DOPENCV_FFMPEG_ENABLE_LIBAVDEVICE=OFF \
  -DVIDEOIO_ENABLE_PLUGINS=OFF \
  -DWITH_GSTREAMER=OFF -DWITH_V4L=OFF -DWITH_OBSENSOR=OFF -DWITH_1394=OFF -DWITH_ARAVIS=OFF \
  -DWITH_XIMEA=OFF -DWITH_UEYE=OFF -DWITH_PVAPI=OFF -DWITH_OPENNI2=OFF -DWITH_LIBREALSENSE=OFF \
  -DWITH_MFX=OFF -DWITH_GPHOTO2=OFF -DWITH_VA=OFF -DWITH_VA_INTEL=OFF \
  -DOPENCV_FORCE_3RDPARTY_BUILD=OFF -DBUILD_ZLIB=OFF -DWITH_ZLIB_NG=OFF \
  -DWITH_PNG=OFF -DWITH_SPNG=OFF -DWITH_JPEG=OFF -DWITH_TIFF=OFF -DWITH_WEBP=OFF \
  -DWITH_OPENJPEG=OFF -DWITH_JASPER=OFF -DWITH_OPENEXR=OFF -DWITH_AVIF=OFF -DWITH_JPEGXL=OFF \
  -DWITH_GDAL=OFF -DWITH_GDCM=OFF \
  -DWITH_IMGCODEC_GIF=OFF -DWITH_IMGCODEC_HDR=OFF -DWITH_IMGCODEC_SUNRASTER=OFF \
  -DWITH_IMGCODEC_PXM=OFF -DWITH_IMGCODEC_PFM=OFF \
  -DWITH_IPP=OFF -DWITH_ITT=OFF -DWITH_OPENCL=OFF \
  -DWITH_OPENCLAMDFFT=OFF -DWITH_OPENCLAMDBLAS=OFF \
  -DWITH_EIGEN=OFF -DWITH_LAPACK=OFF \
  -DWITH_KLEIDICV=OFF -DWITH_CAROTENE=OFF -DWITH_FASTCV=OFF -DWITH_TBB=OFF -DWITH_OPENMP=OFF \
  -DWITH_HARFBUZZ=OFF -DWITH_PROTOBUF=OFF -DWITH_FLATBUFFERS=OFF \
  -DWITH_GTK=OFF -DWITH_QT=OFF -DWITH_VTK=OFF -DWITH_CUDA=OFF \
  -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DBUILD_EXAMPLES=OFF -DBUILD_DOCS=OFF \
  -DBUILD_opencv_apps=OFF -DBUILD_JAVA=OFF -DBUILD_opencv_python3=OFF \
  -DENABLE_CCACHE=OFF -DENABLE_PRECOMPILED_HEADERS=OFF -DENABLE_OMIT_FRAME_POINTER=OFF \
  -DENABLE_CONFIG_VERIFICATION=ON
cmake --build /work/opencv-build -j 4
cmake --install /work/opencv-build

lib=/work/install/lib
ff=/work/ffmpeg-install/lib
libs="$lib/libopencv_videoio.a $lib/libopencv_imgcodecs.a $lib/libopencv_imgproc.a $lib/libopencv_geometry.a $lib/libopencv_flann.a $lib/libopencv_core.a $ff/libavformat.a $ff/libavcodec.a $ff/libswscale.a $ff/libavutil.a"
for archive in $libs; do test -f "$archive"; done
# The built-in FFmpeg backend and the mov demuxer must both be present.
llvm-nm -C $lib/libopencv_videoio.a | grep -q ' T .*cvCreateFileCapture_FFMPEG_proxy'
llvm-nm $ff/libavformat.a | grep -Eq ' [DR] ff_mov_demuxer$'

clang++ -std=c++17 $common -I/work/install/include/opencv5 -c /work/harness.cpp -o /work/harness.o
clang++ -std=c++17 $common -c /work/replay.cpp -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping -fsanitize=address,undefined \
  /work/harness.o /work/replay.o $libs -lz -lm -ldl -lpthread -o /work/replay
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer,address,undefined \
  /work/harness.o $libs -lz -lm -ldl -lpthread -o /work/fuzzer
