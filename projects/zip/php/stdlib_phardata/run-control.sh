#!/bin/sh
set -eu
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /opt/php/bin/php /work/harness.php /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /opt/php/bin/php -object=/opt/libzip/lib/libzip.so -instr-profile=/coverage/control.profdata --sources /work/source/php-8.5.12/ext/phar/zip.c > /coverage/coverage.json
python3 /work/run-control.py
