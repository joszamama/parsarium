#!/bin/sh
set -eu

common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'
cmake -S /work/nabo -B /work/nabo-build \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_CXX_FLAGS="$common" -DCMAKE_INSTALL_PREFIX=/work/install \
  -DEIGEN_INCLUDE_DIR=/work/eigen -DSHARED_LIBS=OFF \
  -DLIBNABO_BUILD_DOXYGEN=OFF -DLIBNABO_BUILD_EXAMPLES=OFF \
  -DLIBNABO_BUILD_TESTS=OFF -DLIBNABO_BUILD_PYTHON=OFF
cmake --build /work/nabo-build --target nabo -j 2
cmake --install /work/nabo-build

# Boost.System is header-only in Ubuntu's Boost 1.90 packages; the pinned
# release still lists it as a separately linked CMake component.
sed -i 's/thread system program_options date_time/thread program_options date_time/g' \
  /work/source/CMakeLists.txt
cmake -S /work/source -B /work/pm-build \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_CXX_FLAGS="$common" -DCMAKE_INSTALL_PREFIX=/work/install \
  -DCMAKE_PREFIX_PATH=/work/install -DLIBNABO_INSTALL_DIR=/work/install \
  -DEIGEN_INCLUDE_DIR=/work/eigen -DBUILD_SHARED_LIBS=ON \
  -DBUILD_EXAMPLES=OFF -DBUILD_EVALUATIONS=OFF \
  -DBUILD_TESTS=OFF -DBUILD_PYTHON_MODULE=OFF
cmake --build /work/pm-build --target pointmatcher -j 2
cmake --install /work/pm-build

clang++ -std=c++17 $common -I/work/source -I/work/eigen \
  -c /work/harness.cpp -o /work/harness.o
clang++ -std=c++17 $common -c /work/replay.cpp -o /work/replay.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o \
  -L/work/install/lib -Wl,-rpath,/work/lib -lpointmatcherd \
  -lyaml-cpp -lboost_thread -lboost_program_options \
  -lboost_date_time -lboost_chrono -o /work/replay

clang++ -std=c++17 $common -c /work/fuzz.cpp -o /work/fuzz.o
clang++ -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o \
  -L/work/install/lib -Wl,-rpath,/work/lib -lpointmatcherd \
  -lyaml-cpp -lboost_thread -lboost_program_options \
  -lboost_date_time -lboost_chrono -o /work/fuzzer
