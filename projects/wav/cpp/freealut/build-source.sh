#!/bin/sh
set -eu
cmake -S /work/source -B /work/build \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DBUILD_STATIC=OFF \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang \
  -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_SHARED_LINKER_FLAGS='-fprofile-instr-generate' \
  -DCMAKE_INSTALL_PREFIX=/work/install
cmake --build /work/build --parallel 6 --target alut
cmake --install /work/build
