#!/bin/sh
set -eu

Xvfb :99 -ac -screen 0 160x120x24 >/tmp/xvfb.log 2>&1 &
i=0
while [ ! -S /tmp/.X11-unix/X99 ]; do
    i=$((i + 1))
    if [ "$i" -ge 100 ]; then cat /tmp/xvfb.log >&2; exit 1; fi
    sleep 0.1
done
export DISPLAY=:99
exec "$@"
