#!/bin/sh
set -eu
common='-O1 -g -fno-omit-frame-pointer -I/work/install/include -L/work/install/lib -lqpdf -Wl,-rpath,/work/install/lib -Wl,-export-dynamic'
clang -fprofile-instr-generate -fcoverage-mapping -c /work/harness.c -I/work/install/include -o /work/harness.o
clang -fprofile-instr-generate -fcoverage-mapping -c /work/replay.c -o /work/replay.o
clang++ -fprofile-instr-generate /work/harness.o /work/replay.o $common -o /work/replay
clang -fsanitize=address,undefined -c /work/harness.c -I/work/install/include -o /work/fuzz-harness.o
clang++ -fsanitize=fuzzer,address,undefined /work/fuzz-harness.o $common -o /work/fuzzer
