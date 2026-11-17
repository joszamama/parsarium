#!/bin/sh
set -eu
# Debian's libtinyxml-dev builds TinyXML with TIXML_USE_STL; do the same.
common='-O1 -g -fno-omit-frame-pointer -DTIXML_USE_STL'
src='/work/source/tinyxml.cpp /work/source/tinyxmlparser.cpp /work/source/tinyxmlerror.cpp /work/source/tinystr.cpp'
clang++ -std=c++17 $common -fprofile-instr-generate -fcoverage-mapping -I/work/source \
  $src /work/harness.cpp /work/replay.cpp -o /work/replay
clang++ -std=c++17 $common -fsanitize=fuzzer,address,undefined -I/work/source \
  $src /work/harness.cpp -o /work/fuzzer
