#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../../../../.." && pwd)"
project_dir="$repo_root/projects/png/python/pygame"
image="parsarium/png-python-pygame-binary-feedback:local"

docker build --quiet -t parsarium/png-python-pygame:local "$project_dir" >/dev/null
docker build --quiet -t "$image" -f "$project_dir/binary-feedback/Dockerfile" "$project_dir/binary-feedback" >/dev/null
docker run --rm --platform linux/amd64 --network none --read-only \
  --tmpfs /tmp:rw,size=64m --cap-drop ALL --security-opt no-new-privileges \
  --user 501:20 -v "$repo_root/controls/png:/controls:ro" \
  --entrypoint /opt/venv/bin/python "$image" /work/binary-smoke.py \
  --module /opt/venv/lib/python3.12/site-packages/pygame.libs/libpng16-bb793e21.so.16.37.0 \
  --control /controls/red-green.png --variant /controls/red-green-title.png \
  --control-output '2x1 first=255,0,0,255' --variant-output '2x1 first=255,0,0,255'
