#!/bin/sh
set -eu
cd /work/source
sed -i '/^static U32 _FORCEINLINE _load4/i U32 _byteswap_ulong(U32 bits);' Source/LibJXR/image/decode/segdec.c
CC=clang CXX=clang++ CFLAGS='-O1 -g -fPIC -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -include unistd.h -include wchar.h -DPNG_ARM_NEON_OPT=0' CXXFLAGS='-O1 -g -fPIC -std=gnu++11 -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -Wno-deprecated-declarations -DPNG_ARM_NEON_OPT=0' \
 make -f Makefile.gnu libfreeimage.a -j 4
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping -I/work/source/Source -c /work/harness.cpp -o /work/harness-cov.o
clang++ $common -fprofile-instr-generate -fcoverage-mapping -I/work/source/Source -c /work/replay.cpp -o /work/replay-cov.o
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness-cov.o /work/replay-cov.o /work/source/libfreeimage.a -lm -o /work/replay
clang++ $common -fsanitize=fuzzer-no-link,address,undefined -I/work/source/Source -c /work/harness.cpp -o /work/harness-fuzz.o
clang++ $common -fsanitize=fuzzer,address,undefined /work/harness-fuzz.o /work/source/libfreeimage.a -lm -o /work/fuzzer
