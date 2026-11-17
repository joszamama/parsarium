"""Check orjson Rust JSON deserializer source feedback on two fixed, valid JSON controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/json/python/orjson'
OVERLAY = ROOT / 'fuzzing/afl-native/json/python/orjson'
REPORT = ROOT / 'data/python/json/orjson-valid-feedback.json'
PREFIX = '/work/orjson-source/src/deserialize/'


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(source: Path, scratch: Path) -> list[str]:
    return ['docker', 'run', '--rm', '--platform', 'linux/arm64', '--network', 'none',
            '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--user', f'{os.getuid()}:{os.getgid()}', '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
            '-v', f'{source}:/input/case:ro', '-v', f'{scratch}:/coverage']


def probe(image: str, source: Path, scratch: Path, label: str) -> tuple[set[str], set[str]]:
    base = sandbox(source, scratch)
    run([*base, '--entrypoint', '/bin/sh', image,
         '/work/afl_trace', '/input/case', f'/coverage/{label}.features'])
    run([*base, '-e', 'AFL_MAP_SIZE=65536', '--entrypoint', 'afl-showmap', image,
         '-m', 'none', '-t', '120000', '-o', f'/coverage/{label}.map',
         '--', '/work/afl_proxy', '/input/case'])
    features = set((scratch / f'{label}.features').read_text().splitlines()) - {''}
    tuples = {line.split(':', 1)[0] for line in
              (scratch / f'{label}.map').read_text().splitlines() if line}
    if not features or not tuples or any(not value.startswith(PREFIX) for value in features):
        raise RuntimeError('feedback is empty or outside orjson deserializer source')
    if not any(value.startswith(PREFIX + 'backend/yyjson.rs:') for value in features):
        raise RuntimeError('orjson backend/yyjson.rs has no feedback')
    return features, tuples


def main() -> None:
    manifest = json.loads((PROJECT / 'manifest.json').read_text())
    base = json.loads((PROJECT / 'verification.json').read_text())
    overlay = json.loads((OVERLAY / 'verification.json').read_text())
    if overlay['base_image_id'] != base['image_id']:
        raise RuntimeError('AFL overlay base differs from verified project')
    control = ROOT / manifest['control']
    variant = ROOT / manifest['differential_control']
    for source, digest in ((control, manifest['control_sha256']),
                           (variant, manifest['differential_control_sha256'])):
        if sha256(source.read_bytes()).hexdigest() != digest:
            raise RuntimeError('valid control hash changed')
    with tempfile.TemporaryDirectory(prefix='parsarium-orjson-feedback-') as temporary:
        scratch = Path(temporary)
        observed = json.loads(run([*sandbox(variant, scratch), '--entrypoint',
                                   '/opt/venv/bin/python', base['image_id'],
                                   '/work/replay.py', '/input/case']))
        if observed != manifest['differential_expected_output']:
            raise RuntimeError(f'valid array structure changed: {observed}')
        first = probe(overlay['image_id'], control, scratch, 'first')
        repeat = probe(overlay['image_id'], control, scratch, 'repeat')
        other = probe(overlay['image_id'], variant, scratch, 'other')
        other_repeat = probe(overlay['image_id'], variant, scratch, 'other-repeat')
    if first != repeat or other != other_repeat:
        raise RuntimeError('repeated orjson Rust JSON deserializer source feedback is unstable')
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    if feature_diff == 0 or tuple_diff == 0:
        raise RuntimeError('orjson/AFL feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'json/python/orjson', 'pass': True,
              'input_kind': 'two fixed valid RFC 8259 JSON controls',
              'feedback_scope': 'native orjson 3.13.0 Rust deserializer source regions; vendored yyjson C parser excluded',
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'variant_output': observed,
              'control_repeat_identical': True, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'parser_feature_difference': feature_diff,
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
