#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../../../../.." && pwd)"
project_dir="$repo_root/projects/ascii_pnm/python/pyqt5"
image="parsarium/ascii_pnm-python-pyqt5-binary-feedback:local"

cd "$repo_root"
python3 - "$project_dir" "$image" <<'PY'
import subprocess
import sys
from scripts.docker_slots import docker_build_slot

project_dir, image = sys.argv[1:]
with docker_build_slot():
    subprocess.run(["docker", "build", "--quiet", "--platform", "linux/amd64",
                    "-t", "parsarium/ascii_pnm-python-pyqt5:local", project_dir],
                   stdout=subprocess.DEVNULL, check=True)
    subprocess.run(["docker", "build", "--quiet", "--platform", "linux/amd64",
                    "-t", image, "-f", f"{project_dir}/binary-feedback/Dockerfile",
                    f"{project_dir}/binary-feedback"],
                   stdout=subprocess.DEVNULL, check=True)
PY
docker run --rm --platform linux/amd64 --network none --read-only \
  --tmpfs /tmp:rw,size=64m --cap-drop ALL --security-opt no-new-privileges \
  --user "$(id -u):$(id -g)" -v "$repo_root/controls/ascii_pnm:/controls:ro" \
  --entrypoint /opt/venv/bin/python "$image" /work/binary-smoke.py \
  --module /opt/venv/lib/python3.14/site-packages/PyQt5/Qt5/lib/libQt5Gui.so.5 \
  --control /controls/red-green.ppm --variant /controls/black-white.pgm \
  --control-output '2x1 first=255,0,0' --variant-output '2x1 first=0,0,0'
