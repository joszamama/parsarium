#!/bin/sh
set -eu
cmake -S /work/source -B /work/build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_C_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_CXX_FLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' \
  -DCMAKE_SHARED_LINKER_FLAGS='-fprofile-instr-generate' \
  -DBUILD_STATIC_LIBS=OFF -DBUILD_SHARED_LIBS=ON -DBUILD_DOC=OFF \
  -DREQUIRE_CRYPTO_NATIVE=ON -DINSTALL_EXAMPLES=OFF -DCMAKE_INSTALL_PREFIX=/work/install
cmake --build /work/build --parallel 6 --target libqpdf
cmake --install /work/build --component lib
cmake --install /work/build --component dev
