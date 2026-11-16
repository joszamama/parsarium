#!/bin/sh
set -eu
LLVM_PROFILE_FILE=/coverage/control.profraw /usr/bin/python3 /work/http-replay.py /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /opt/php/bin/php -instr-profile=/coverage/control.profdata --sources /work/source/php-8.5.12/sapi/cli/php_http_parser.c > /coverage/coverage.json
python3 /work/run-control.py
