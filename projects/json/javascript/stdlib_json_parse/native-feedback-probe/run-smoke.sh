#!/usr/bin/env bash
# Repeatable, scoped native feedback for V8 JSON.parse: v8::internal::JsonParser<...> function entries
# (gdb one-shot breakpoints on the pinned node binary's symbols). Not source lines, not AFL++ edges.
set -euo pipefail
repo_root="$(cd "$(dirname "$0")/../../../../.." && pwd)"
project_dir="$repo_root/projects/json/javascript/stdlib_json_parse"
image="parsarium/json-javascript-stdlib_json_parse-native-feedback:local"
docker build --quiet -t parsarium/json-javascript-stdlib_json_parse:local "$project_dir" >/dev/null
docker build --quiet -t "$image" "$project_dir/native-feedback-probe" >/dev/null
probe() {
  docker run --rm --platform linux/arm64 --network none --read-only --tmpfs /tmp:rw,size=64m \
    --cap-drop ALL --cap-add SYS_PTRACE --security-opt seccomp=unconfined \
    -v "$repo_root/controls/json:/controls:ro" "$image" "$1"
}
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
probe /controls/nested-object.json > "$work/control-1"
probe /controls/nested-object.json > "$work/control-2"
probe /controls/nested-array.json > "$work/variant"
probe --baseline > "$work/baseline"
docker run --rm --entrypoint cat "$image" /work/gdb-version.txt > "$work/gdb"
python3 - "$work" <<'PY'
import json, sys
from pathlib import Path
work = Path(sys.argv[1])
def hits(name):
    lines = (work / name).read_text().splitlines()
    return lines[0].split()[1], [line[4:] for line in lines[1:]]
symbols, control = hits("control-1")
_, repeat = hits("control-2")
_, variant = hits("variant")
_, baseline = hits("baseline")
print(json.dumps({
    "feedback_kind": "native_function_entries_not_source_coverage",
    "tool": (work / "gdb").read_text().strip(),
    "scope": "v8::internal::JsonParser<...> text symbols in /usr/local/bin/node",
    "scope_symbols": int(symbols),
    "baseline_functions": len(baseline),
    "control_functions": len(control),
    "repeat_identical": control == repeat,
    "variant_functions": len(variant),
    "variant_differs": control != variant,
    "control_only": sorted(set(control) - set(variant)),
    "variant_only": sorted(set(variant) - set(control)),
}, indent=2))
PY
