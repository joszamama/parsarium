#!/bin/sh
set -eu
# LLVM tools link the system libxml2; keep them off the instrumented /opt/libxml2 build.
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /opt/php/bin/php /work/harness.php /input/control > /coverage/observed.json
env -u LD_LIBRARY_PATH llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
env -u LD_LIBRARY_PATH llvm-cov export /opt/php/bin/php -object /opt/libxml2/lib/libxml2.so.16 -instr-profile=/coverage/control.profdata \
    --sources /work/source/php-8.5.12/ext/simplexml /work/source/php-8.5.12/ext/libxml /work/source/libxml2-2.15.4 > /coverage/coverage.json
python3 /work/run-control.py
