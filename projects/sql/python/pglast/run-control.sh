#!/bin/sh
set -eu
export LLVM_PROFILE_FILE=/coverage/native.profraw
/opt/venv/bin/python /work/run-control.py
llvm-profdata merge /coverage/native.profraw -o /coverage/native.profdata
module=$(find /opt/venv/lib/python3.14/site-packages/pglast -maxdepth 1 -name 'parser*.so' -print -quit)
test -n "$module"
llvm-cov export "$module" -instr-profile=/coverage/native.profdata -skip-expansions -skip-functions > /coverage/native.json
/opt/venv/bin/python /work/merge-native-coverage.py
