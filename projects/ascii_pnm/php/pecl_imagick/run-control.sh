#!/bin/sh
set -eu
LLVM_PROFILE_FILE=/coverage/control.profraw /usr/bin/php -d extension=/opt/imagick/imagick.so /work/control.php /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /opt/imagick/imagick.so -instr-profile=/coverage/control.profdata --sources /work/source/imagick-3.8.1/imagick_class.c > /coverage/coverage.json
python3 /work/run-control.py
