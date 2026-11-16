#!/bin/sh
set -eu
cmake -S /work/source/csfml -B /work/build/csfml -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_CXX_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_PREFIX_PATH=/work/install -DCMAKE_INSTALL_PREFIX=/work/install \
  -DCSFML_BUILD_WINDOW=OFF -DCSFML_BUILD_GRAPHICS=OFF -DCSFML_BUILD_AUDIO=ON \
  -DCSFML_BUILD_NETWORK=OFF -DCSFML_BUILD_EXAMPLES=OFF -DCSFML_BUILD_TEST_SUITE=OFF
cmake --build /work/build/csfml -j 6
cmake --install /work/build/csfml
