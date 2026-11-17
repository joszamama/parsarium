#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../../../../.." && pwd)"
project_dir="$repo_root/projects/mp3/python/pygame"
image="parsarium/mp3-python-pygame-binary-feedback:local"

docker build --quiet -t parsarium/mp3-python-pygame:local "$project_dir" >/dev/null
docker build --quiet -t "$image" -f "$project_dir/binary-feedback/Dockerfile" "$project_dir/binary-feedback" >/dev/null
docker run --rm --platform linux/amd64 --network none --read-only \
  --tmpfs /tmp:rw,size=64m --cap-drop ALL --security-opt no-new-privileges \
  --user 501:20 -v "$repo_root/controls/mp3:/controls:ro" \
  --entrypoint /opt/venv/bin/python "$image" /work/binary-smoke.py \
  --module /opt/venv/lib/python3.12/site-packages/pygame.libs/libmpg123-fad61782.so.0.47.0 \
  --control /controls/id3v2-tagged-tone.mp3 --variant /controls/id3v2-tagged-tone-v24.mp3 \
  --control-output 'duration_ms=1000' --variant-output 'duration_ms=1000'
