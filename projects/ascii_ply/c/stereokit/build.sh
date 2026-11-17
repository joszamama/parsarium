#!/bin/sh
set -eu
mode=${PARSARIUM_BUILD:-coverage}
step=${1:-both}
export DEBIAN_FRONTEND=noninteractive
export LLVM_PROFILE_FILE=/tmp/parsarium-build-%m.profraw
case "$mode" in
coverage)
  c_compiler=clang
  cxx_compiler=clang++
  common='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping -fsanitize=fuzzer-no-link'
  link_flags='-fprofile-instr-generate'
  ;;
afl)
  c_compiler=afl-clang-fast
  cxx_compiler=afl-clang-fast++
  common='-O1 -g -fno-omit-frame-pointer'
  link_flags=''
  # micro_ply's implementation is included in model_ply.cpp. Exclude every
  # graphics, dependency, and adapter translation unit from AFL's edge map.
  printf 'src:model_ply.cpp\n' > /work/afl-allowlist.txt
  export AFL_LLVM_INSTRUMENT=CLASSIC AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  ;;
*) echo "unknown PARSARIUM_BUILD: $mode" >&2; exit 2 ;;
esac
if [ "$step" = source ] || [ "$step" = both ]; then
python3 - <<'PY'
from pathlib import Path
header = Path('/work/source/StereoKitC/stereokit.h').read_text()
old = 'quit_reason_ quitReason = quit_reason_user'
assert header.count(old) == 1
Path('/work/stereokit_c_compat.h').write_text(header.replace(old, 'quit_reason_ quitReason'))
PY
cmake -S /work/source -B /work/build -G Ninja \
  -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER="$c_compiler" \
  -DCMAKE_CXX_COMPILER="$cxx_compiler" \
  -DCMAKE_C_FLAGS="$common" -DCMAKE_CXX_FLAGS="$common" \
  -DCMAKE_SHARED_LINKER_FLAGS="$link_flags" \
  -DSK_BUILD_TESTS=OFF -DSK_PHYSICS=OFF -DSK_BUILD_SHARED_LIBS=ON
cmake --build /work/build --target StereoKitC -j 4
mkdir -p /work/lib
cp /work/build/libStereoKitC.so /work/lib/
if [ "$mode" = coverage ]; then
  readelf -SW /work/lib/libStereoKitC.so | grep -q __llvm_covmap
fi
fi
if [ "$step" = harness ] || [ "$step" = both ]; then
if [ "$mode" = coverage ]; then
  "$c_compiler" -std=c11 $common -I/work /work/harness.c /work/replay.c \
    -L/work/lib -Wl,-rpath,/work/lib -lStereoKitC -lstdc++ -lm -o /work/replay
  "$c_compiler" -std=c11 -O1 -g -fsanitize=fuzzer,address,undefined -I/work \
    /work/harness.c -L/work/lib -Wl,-rpath,/work/lib -lStereoKitC -lstdc++ -lm -o /work/fuzzer
else
  "$c_compiler" -std=c11 $common -I/work /work/harness.c /work/replay.c \
    -L/work/lib -Wl,-rpath,/work/lib -lStereoKitC -lstdc++ -lm -o /work/replay
  "$c_compiler" -std=c11 -O1 -g -fsanitize=fuzzer,address,undefined -fno-sanitize=function \
    -I/work /work/harness.c -L/work/lib -Wl,-rpath,/work/lib \
    -lStereoKitC -lstdc++ -lm -o /work/fuzzer
fi
fi
