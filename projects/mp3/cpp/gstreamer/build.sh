#!/bin/sh
set -eu
export PKG_CONFIG_PATH=/work/install/lib/pkgconfig
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping $(pkg-config --cflags gstreamer-pbutils-1.0) /work/harness.cpp /work/replay.cpp $(pkg-config --libs gstreamer-pbutils-1.0) -Wl,-rpath,/work/install/lib -Wl,-export-dynamic -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined $(pkg-config --cflags gstreamer-pbutils-1.0) /work/harness.cpp $(pkg-config --libs gstreamer-pbutils-1.0) -Wl,-rpath,/work/install/lib -Wl,-export-dynamic -o /work/fuzzer
