#!/bin/sh
set -eu
# One PHP process runs the documented setInputString()/parse() call with Xdebug line coverage of the package and
# LLVM source coverage of ext/xml and libxml2. LLVM tools link the system libxml2; keep them off /opt/libxml2.
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /opt/php/bin/php -d xdebug.mode=coverage /work/run-control.php coverage
# setInputFile()/setInput() cross-check in a separate process, so its parses do not enter the line counts.
LLVM_PROFILE_FILE=/tmp/crosscheck-%m.profraw /opt/php/bin/php /work/run-control.php crosscheck > /coverage/crosscheck.json
env -u LD_LIBRARY_PATH llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
env -u LD_LIBRARY_PATH llvm-cov export /opt/php/bin/php -object /opt/libxml2/lib/libxml2.so.16 -instr-profile=/coverage/control.profdata \
    --sources /work/source/php-8.5.12/ext/xml /work/source/php-8.5.12/ext/libxml /work/source/libxml2-2.15.4 > /coverage/native.json
python3 /work/run-control.py
