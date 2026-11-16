#!/bin/sh
set -eu
CC=clang CFLAGS='-O1 -g -fprofile-instr-generate -fcoverage-mapping' cmake -S /work/source -B /work/physfs-build \
 -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DPHYSFS_BUILD_STATIC=ON -DPHYSFS_BUILD_SHARED=OFF -DPHYSFS_BUILD_TEST=OFF \
 -DPHYSFS_BUILD_DOCS=OFF -DPHYSFS_ARCHIVE_ZIP=ON -DPHYSFS_ARCHIVE_7Z=OFF
cmake --build /work/physfs-build --target physfs-static -j 2
common='-O1 -g -fno-omit-frame-pointer -I/work/source/src'
clang $common -fprofile-instr-generate -fcoverage-mapping /work/harness.c /work/replay.c /work/physfs-build/libphysfs.a -lz -o /work/replay
clang $common -fsanitize=fuzzer,address,undefined /work/harness.c /work/physfs-build/libphysfs.a -lz -o /work/fuzzer
