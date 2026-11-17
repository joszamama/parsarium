#!/bin/sh
set -eu

export LLVM_PROFILE_FILE=/coverage/control.profraw
/opt/venv/bin/python /work/replay.py /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
module=$(find /opt/venv/lib/python3.10/site-packages/http_parser -name 'parser.cpython-*.so' -print -quit)
test -n "$module"
llvm-cov export "$module" -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
/opt/venv/bin/python /work/run-control.py
