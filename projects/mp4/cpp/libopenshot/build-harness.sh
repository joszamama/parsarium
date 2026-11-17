#!/bin/sh
set -eu
mode=${PARSARIUM_BUILD:-coverage}
# FFmpegReader.h pulls in Clip.h, Frame.h, and Qt/JUCE headers whose class
# layout depends on PUBLIC definitions such as USE_HW_ACCEL and USE_OPENCV.
# Reuse the exact defines, include paths, and language flags CMake used for
# libopenshot's own FFmpegReader.cpp so the harness agrees with the library.
lib_flags=$(python3 - <<'PY'
import json, shlex
entries = json.load(open('/work/libopenshot-build/compile_commands.json'))
entry, = [e for e in entries if e['file'].endswith('/src/FFmpegReader.cpp')]
args = entry.get('arguments') or shlex.split(entry['command'])
keep, take_next = [], False
for arg in args:
    if take_next:
        keep.append(arg); take_next = False
    elif arg in ('-isystem', '-I', '-D'):
        keep.append(arg); take_next = True
    elif arg == '-Dopenshot_EXPORTS':
        continue
    elif arg.startswith(('-D', '-I', '-isystem', '-std=', '-fopenmp', '-fPIC')):
        keep.append(arg)
print(shlex.join(keep))
PY
)
eval "set -- $lib_flags"
common='-O1 -g -fno-omit-frame-pointer'
libs='-L/work/install/lib -Wl,-rpath,/work/install/lib -lopenshot -lopenshot-audio -lavformat -lavcodec -lavutil -lQt6Gui -lQt6Core -fopenmp'
case "$mode" in
coverage)
  clang++ $common -fprofile-instr-generate -fcoverage-mapping "$@" \
    /work/harness.cpp /work/replay.cpp $libs -o /work/replay
  clang++ $common -fsanitize=fuzzer,address,undefined -fno-sanitize=function "$@" \
    /work/harness.cpp $libs -o /work/fuzzer
  ;;
afl)
  printf 'src:mov.c\nsrc:FFmpegReader.cpp\n' > /work/afl-allowlist.txt
  export AFL_LLVM_INSTRUMENT=CLASSIC AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt
  afl-clang-fast++ $common "$@" /work/harness.cpp /work/replay.cpp $libs -o /work/replay
  afl-clang-fast++ $common -fsanitize=fuzzer,address,undefined -fno-sanitize=function "$@" \
    /work/harness.cpp $libs -o /work/fuzzer
  ;;
*) echo "unknown PARSARIUM_BUILD: $mode" >&2; exit 2 ;;
esac
