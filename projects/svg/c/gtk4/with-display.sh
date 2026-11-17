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
export XDG_CACHE_HOME=/tmp
# SVG parsing does not need a graphics renderer. Disabling these display
# features keeps the AFL edge map stable across one-file invocations.
export GDK_DISABLE=gl,vulkan,dmabuf,threads
export GSK_RENDERER=cairo
exec "$@"
