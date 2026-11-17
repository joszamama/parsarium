#!/bin/sh
set -eu
# One PHP process runs yaml_parse() on the control; yaml.so and libyaml.so write LLVM profiles.
# LLVM tools must not pick up the instrumented /opt/libyaml build.
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /opt/php/bin/php /work/harness.php /input/control > /coverage/observed.json
env -u LD_LIBRARY_PATH llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
env -u LD_LIBRARY_PATH llvm-cov export "$(/opt/php/bin/php-config --extension-dir)/yaml.so" \
    -object /opt/libyaml/lib/libyaml-0.so.2 -instr-profile=/coverage/control.profdata \
    --sources /work/source/pecl-yaml-2.3.0 /work/source/yaml-0.2.5 > /coverage/coverage.json
python3 /work/run-control.py
