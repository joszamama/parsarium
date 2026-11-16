#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../../../../.." && pwd)"
project_dir="$repo_root/projects/ascii_pnm/python/pyqt6"
image="parsarium/ascii_pnm-python-pyqt6-binary-feedback:local"

docker build --quiet -t parsarium/ascii_pnm-python-pyqt6:local "$project_dir" >/dev/null
docker build --quiet -t "$image" -f "$project_dir/binary-feedback/Dockerfile" "$project_dir/binary-feedback" >/dev/null
docker run --rm --platform linux/amd64 --network none --read-only \
  --tmpfs /tmp:rw,size=64m --cap-drop ALL --security-opt no-new-privileges \
  --user 501:20 -v "$repo_root/controls/ascii_pnm:/controls:ro" \
  --entrypoint /opt/venv/bin/python "$image" /work/binary-smoke.py \
  --module /opt/venv/lib/python3.14/site-packages/PyQt6/Qt6/lib/libQt6Gui.so.6 \
  --control /controls/red-green.ppm --variant /controls/black-white.pgm \
  --control-output '2x1 first=255,0,0' --variant-output '2x1 first=0,0,0'
