#!/bin/sh
set -eu
export PATH=/work/qt/bin:$PATH
CC=clang CXX=clang++ CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' CXXFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
 cmake -S /work/source -B /work/build -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_PREFIX_PATH=/work/qt -DCMAKE_INSTALL_PREFIX=/work/qt -DQT_BUILD_TESTS=OFF -DQT_BUILD_EXAMPLES=OFF
cmake --build /work/build -j 4
cmake --install /work/build
common='-O1 -g -fno-omit-frame-pointer'
includes='-I/work/qt/include -I/work/qt/include/QtCore -I/work/qt/include/QtGui -I/work/qt/include/QtSvg'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $includes /work/harness.cpp /work/replay.cpp -L/work/qt/lib -Wl,-rpath,/work/qt/lib -lQt6Svg -lQt6Gui -lQt6Core -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $includes /work/harness.cpp -L/work/qt/lib -Wl,-rpath,/work/qt/lib -lQt6Svg -lQt6Gui -lQt6Core -o /work/fuzzer
