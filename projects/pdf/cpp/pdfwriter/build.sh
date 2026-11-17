#!/bin/sh
set -eu
# The PDF-Writer build stays in build.sh so the AFL++ overlay's compiler
# rewrite instruments the parser library, not only the harness. Two static
# builds: LLVM source coverage for replay, ASan/UBSan for the fuzzer.
# DCT, TIFF, and PNG image codecs are disabled; none is on the
# StartPDFParsing/GetPagesCount path. FreeType and zlib come from the system;
# LibAesgm (PDF decryption) is the bundled copy, as in the catalog build.
pdfwriter() {
  cmake -S /work/source -B "$1" -G Ninja -DCMAKE_BUILD_TYPE= \
    -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_C_FLAGS="$2" -DCMAKE_CXX_FLAGS="$2" -DBUILD_SHARED_LIBS=OFF \
    -DUSE_BUNDLED=FALSE -DUSE_UNBUNDLED_FALLBACK_BUNDLED=TRUE \
    -DPDFHUMMUS_NO_DCT=TRUE -DPDFHUMMUS_NO_TIFF=TRUE -DPDFHUMMUS_NO_PNG=TRUE
  cmake --build "$1" --parallel 6 --target PDFWriter LibAesgm
}
pdfwriter /work/build-coverage '-O1 -g -fprofile-instr-generate -fcoverage-mapping'
pdfwriter /work/build-fuzz '-O1 -g -fno-omit-frame-pointer -fsanitize=fuzzer-no-link -fsanitize=address,undefined'
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -I/work/source/PDFWriter -DPDFHUMMUS_NO_DCT=1 -DPDFHUMMUS_NO_TIFF=1 -DPDFHUMMUS_NO_PNG=1'
clang++ -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp /work/replay.cpp $common \
  /work/build-coverage/PDFWriter/libPDFWriter.a /work/build-coverage/LibAesgm/libLibAesgm.a -lfreetype -lz -o /work/replay
clang++ -fsanitize=fuzzer,address,undefined /work/harness.cpp $common \
  /work/build-fuzz/PDFWriter/libPDFWriter.a /work/build-fuzz/LibAesgm/libLibAesgm.a -lfreetype -lz -o /work/fuzzer
