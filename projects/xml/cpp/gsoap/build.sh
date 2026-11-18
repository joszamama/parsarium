#!/bin/sh
set -eu
# DOM-only gSOAP build as documented in gsoap/samples/dom/README.md ("soapcpp2 -CSL import/dom.h", then
# compile the application with soapC.cpp, dom.cpp and stdsoap2.cpp). soapcpp2 is built from the same
# pinned source (its bison/flex outputs ship pre-generated); the generated soapC.cpp, soapH.h,
# soapStub.h and soap.nsmap are written to /work/gen, outside the measured parser sources.
src=/work/source/gsoap
cd $src/src
clang -O1 -w -o /work/soapcpp2 soapcpp2.c symbol2.c error2.c init2.c soapcpp2_yacc.tab.c lex.yy.c
mkdir -p /work/gen
cd /work/gen
/work/soapcpp2 -CSL -I$src/import $src/import/dom.h
common='-O1 -g -fno-omit-frame-pointer'
inc="-I/work/gen -I$src"
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping $inc \
  $src/stdsoap2.cpp $src/dom.cpp /work/gen/soapC.cpp /work/harness.cpp /work/replay.cpp -o /work/replay
# stdsoap2.cpp's allocator writes and checks a 4-byte canary after each soap_malloc block at an unaligned
# offset (soap_malloc/soap_dealloc), which UBSan's alignment check reports on every valid parse; that one
# check is disabled so the fuzz target runs.
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -fno-sanitize=alignment $inc \
  $src/stdsoap2.cpp $src/dom.cpp /work/gen/soapC.cpp /work/harness.cpp -o /work/fuzzer
