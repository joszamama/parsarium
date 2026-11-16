#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../../../../.." && pwd)"
project_dir="$repo_root/projects/ascii_pnm/python/pygame"
image="parsarium/ascii_pnm-python-pygame-binary-feedback:local"

docker build --quiet -t parsarium/ascii_pnm-python-pygame:local "$project_dir" >/dev/null
docker build --quiet -t "$image" -f "$project_dir/binary-feedback/Dockerfile" "$project_dir/binary-feedback" >/dev/null
docker run --rm --platform linux/amd64 --network none --read-only \
  --tmpfs /tmp:rw,size=64m --cap-drop ALL --security-opt no-new-privileges \
  --user 501:20 -v "$repo_root/controls/ascii_pnm:/controls:ro" \
  --entrypoint /opt/venv/bin/python "$image" /work/binary-smoke.py \
  --module /opt/venv/lib/python3.12/site-packages/pygame.libs/libSDL2_image-2-6bbdaa8d.0.so.0.2.3 \
  --control /controls/red-green.ppm --variant /controls/black-white.pgm \
  --control-output '2x1 first=255,0,0' --variant-output '2x1 first=0,0,0'
