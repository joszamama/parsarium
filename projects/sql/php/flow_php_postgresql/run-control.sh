#!/bin/sh
set -eu
# One PHP process runs sql_parse() and the Traverser summary with Xdebug line coverage of the package and LLVM
# source coverage of ext/pg_query.c and libpg_query (both in pg_query.so).
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /opt/php/bin/php -d xdebug.mode=coverage /work/run-control.php
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export "$(/opt/php/bin/php-config --extension-dir)/pg_query.so" -instr-profile=/coverage/control.profdata \
    --sources /work/source/pg-query-ext-0.48.0/ext /work/source/libpg_query-18.0.0 > /coverage/native.json
python3 /work/run-control.py
