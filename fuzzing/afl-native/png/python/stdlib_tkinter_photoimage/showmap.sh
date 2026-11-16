#!/bin/sh
set -eu

# Keep Xvfb outside the AFL target process, which is the Python launcher.
exec /work/with-display.sh afl-showmap "$@"
