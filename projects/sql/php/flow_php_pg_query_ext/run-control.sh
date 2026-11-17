#!/bin/sh
set -eu
# One PHP process runs pg_query_parse() on the control; pg_query.so (the extension with libpg_query linked in
# statically) writes an LLVM profile.
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /opt/php/bin/php /work/harness.php /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export "$(/opt/php/bin/php-config --extension-dir)/pg_query.so" -instr-profile=/coverage/control.profdata \
    --sources /work/source/pg-query-ext-0.48.0/ext /work/source/libpg_query-18.0.0 > /coverage/coverage.json
python3 /work/run-control.py
