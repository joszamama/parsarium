#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
cmake -S /work/source -B /work/build \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DPCL_SHARED_LIBS=ON -DWITH_VTK=OFF -DWITH_QT=NO -DWITH_OPENGL=OFF \
  -DWITH_GLEW=OFF -DWITH_LIBUSB=OFF -DWITH_PCAP=OFF -DWITH_PNG=OFF \
  -DWITH_QHULL=OFF -DBUILD_examples=OFF -DBUILD_tools=OFF \
  -DBUILD_apps=OFF -DBUILD_global_tests=OFF
cmake --build /work/build --target pcl_io -j 2

includes='-I/work/source/common/include -I/work/source/io/include -I/work/source/octree/include -I/work/build/include -I/usr/include/eigen3'
clang++ -std=c++17 $common $includes -c /work/harness.cpp -o /work/harness.o
clang++ -std=c++17 $common -c /work/replay.cpp -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o \
  -L/work/build/lib -Wl,-rpath,/work/lib -lpcl_io -lpcl_io_ply \
  -lpcl_octree -lpcl_common -lboost_iostreams -o /work/replay

clang++ -std=c++17 $common -c /work/fuzz.cpp -o /work/fuzz.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o \
  -L/work/build/lib -Wl,-rpath,/work/lib -lpcl_io -lpcl_io_ply \
  -lpcl_octree -lpcl_common -lboost_iostreams -o /work/fuzzer
