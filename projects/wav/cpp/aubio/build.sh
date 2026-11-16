#!/bin/sh
set -eu
cd /work/source
python3 - <<'PY'
from pathlib import Path
p = Path('waflib/Context.py')
s = p.read_text().replace('import os,re,imp,sys', 'import os,re,sys,types').replace('imp.new_module(WSCRIPT_FILE)', 'types.ModuleType(WSCRIPT_FILE)')
p.write_text(s)
for p in Path('waflib').rglob('*.py'):
    s = p.read_text()
    t = s.replace("'rU'", "'r'").replace('"rU"', '"r"')
    if s != t:
        p.write_text(t)
PY
export CC=clang
export CFLAGS='-O1 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping'
python3 waf configure --prefix=/work/install --disable-avcodec --enable-sndfile --disable-jack --disable-samplerate --disable-docs --disable-tests --disable-examples
python3 waf build --disable-tests --disable-examples -j 4
common='-O1 -g -fno-omit-frame-pointer'
clang++ $common -fprofile-instr-generate -fcoverage-mapping -I/work/source/src /work/harness.cpp /work/replay.cpp /work/source/build/src/libaubio.a $(pkg-config --libs sndfile) -lm -o /work/replay
clang++ $common -fsanitize=fuzzer,address,undefined -I/work/source/src /work/harness.cpp /work/source/build/src/libaubio.a $(pkg-config --libs sndfile) -lm -o /work/fuzzer
