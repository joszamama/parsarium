#!/usr/bin/env bash
# V8 JSON.parse source-line feedback: builds Node.js 26.10.0 from the official tarball with only
# deps/v8/src/json/json-parser.cc under Clang source-based coverage, then replays node -e 0 and both
# valid controls twice each. Prints the measurement JSON plus the image ID. The first build compiles
# all of Node.js (about 25 minutes on 12 cores) and is cached afterwards.
set -euo pipefail
repo_root="$(cd "$(dirname "$0")/../../../../.." && pwd)"
project_dir="$repo_root/projects/json/javascript/stdlib_json_parse"
image="parsarium/json-javascript-stdlib_json_parse-source-coverage:local"
docker build --quiet --platform linux/arm64 -t "$image" -f "$project_dir/source-coverage/Dockerfile" "$project_dir" >/dev/null
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
docker run --rm --pull never --platform linux/arm64 --network none --read-only --tmpfs /tmp:rw,size=64m \
  --cap-drop ALL --security-opt no-new-privileges --user "$(id -u):$(id -g)" \
  -v "$repo_root/controls/json:/controls:ro" -v "$work:/coverage" "$image" > /dev/null
python3 - "$work/summary.json" "$(docker image inspect "$image" --format '{{.Id}}')" <<'PY'
import json, sys
summary = json.load(open(sys.argv[1]))
print(json.dumps({"image_id": sys.argv[2], **summary}, indent=2))
PY
