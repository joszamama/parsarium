#!/bin/sh
set -eu
# Header-only Boost.JSON: harness.cpp includes <boost/json/src.hpp> once.
common='-std=c++17 -O1 -g -fno-omit-frame-pointer -DBOOST_ALL_NO_LIB -I/work/source -I/work/boost'
clang++ $common -fprofile-instr-generate -fcoverage-mapping /work/harness.cpp -o /work/replay
clang++ $common -DPARSARIUM_FUZZER -fsanitize=fuzzer,address,undefined /work/harness.cpp -o /work/fuzzer
