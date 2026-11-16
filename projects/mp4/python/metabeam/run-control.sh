#!/bin/sh
set -eu
export LLVM_PROFILE_FILE=/coverage/native.profraw
/opt/venv/bin/python /work/run-control.py
/work/llvm-profdata merge /coverage/native.profraw -o /coverage/native.profdata
module=$(find /opt/venv/lib/python3.13/site-packages/metabeam -maxdepth 1 -name '_metabeam*.so' -print -quit)
test -n "$module"
/work/llvm-cov export "$module" -instr-profile=/coverage/native.profdata > /coverage/native.json
/opt/venv/bin/python /work/merge-native-coverage.py
