#!/bin/sh
set -eu
cmake -S /work/source/sfml -B /work/build/sfml -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_CXX_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_INSTALL_PREFIX=/work/install \
  -DSFML_BUILD_WINDOW=OFF -DSFML_BUILD_GRAPHICS=OFF -DSFML_BUILD_AUDIO=ON \
  -DSFML_BUILD_NETWORK=OFF -DSFML_USE_SYSTEM_DEPS=ON -DBUILD_SHARED_LIBS=ON \
  -DSFML_BUILD_EXAMPLES=OFF -DSFML_BUILD_TEST_SUITE=OFF
cmake --build /work/build/sfml -j 6
cmake --install /work/build/sfml
