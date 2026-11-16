#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../../../../.." && pwd)"
project_dir="$repo_root/projects/wav/python/pygame"
image="parsarium/wav-python-pygame-binary-feedback:local"

docker build --quiet -t parsarium/wav-python-pygame:local "$project_dir" >/dev/null
docker build --quiet -t "$image" -f "$project_dir/binary-feedback/Dockerfile" "$project_dir/binary-feedback" >/dev/null
docker run --rm --platform linux/amd64 --network none --read-only \
  --tmpfs /tmp:rw,size=64m --cap-drop ALL --security-opt no-new-privileges \
  --user 501:20 -v "$repo_root/controls/wav:/controls:ro" \
  -v "$project_dir/binary-feedback:/variants:ro" \
  --entrypoint /opt/venv/bin/python "$image" /work/binary-smoke.py \
  --module /opt/venv/lib/python3.12/site-packages/pygame.libs/libSDL2_mixer-2-673d03d7.0.so.0.600.3 \
  --control /controls/four-samples.wav --variant /variants/stereo-8bit.wav \
  --control-output '8000Hz/1ch samples=4' --variant-output '8000Hz/1ch samples=2'
