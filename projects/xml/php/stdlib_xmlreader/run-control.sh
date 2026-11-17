#!/bin/sh
set -eu
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /opt/php/bin/php /work/harness.php /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /opt/php/bin/php -object /opt/libxml2/lib/libxml2.so.16 -instr-profile=/coverage/control.profdata \
    --sources /work/source/php-8.5.12/ext/xmlreader /work/source/php-8.5.12/ext/libxml /work/source/libxml2-2.15.4 > /coverage/coverage.json
python3 /work/run-control.py
