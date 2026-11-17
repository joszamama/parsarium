#!/bin/sh
set -eu

# facil.io 0.7.6's HTTP/1 parser is header-only: harness.c includes the pinned
# lib/facil/http/parsers/http1_parser.h, so the parser stages are compiled in
# the harness object with the same instrumentation: LLVM source coverage for
# replay and sanitizer coverage for the fuzzer. No other facil.io source is
# compiled or linked.
common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link,address,undefined'

clang -std=c11 -Wall -Wextra $common -I/work/source -c /work/harness.c -o /work/harness.o
clang -std=c11 -Wall -Wextra $common -c /work/replay.c -o /work/replay.o
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=address,undefined /work/harness.o /work/replay.o -o /work/replay

clang -std=c11 -Wall -Wextra $common -c /work/fuzz.c -o /work/fuzz.o
clang -O1 -g -fprofile-instr-generate -fcoverage-mapping \
  -fsanitize=fuzzer,address,undefined /work/harness.o /work/fuzz.o -o /work/fuzzer
