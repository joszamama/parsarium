#!/bin/sh
set -eu

python -m venv /opt/venv
/opt/venv/bin/python -m pip install --no-index --no-deps /work/atheris-2.3.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
cd /work/source
CC=clang CFLAGS='-O0 -g -fno-omit-frame-pointer -fprofile-instr-generate -fcoverage-mapping' \
  LDFLAGS='-fprofile-instr-generate' \
  /opt/venv/bin/python -m pip install --no-build-isolation --no-deps .
/opt/venv/bin/python - <<'PY'
import http_parser.parser as parser
assert parser.__file__.endswith('linux-gnu.so'), parser.__file__
print(parser.__file__)
PY
