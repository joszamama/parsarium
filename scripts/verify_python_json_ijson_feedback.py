"""Check ijson yajl2_c/yajl source feedback on two fixed, valid JSON controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/json/python/ijson'
OVERLAY = ROOT / 'fuzzing/afl-native/json/python/ijson'
REPORT = ROOT / 'data/python/json/ijson-valid-feedback.json'
PREFIX = '/work/ijson-source/'
YAJL = PREFIX + 'yajl-patched-sources/src/'
IJSON_EXT = PREFIX + 'src/ijson/backends/ext/_yajl2/'
REQUIRED = (YAJL + 'yajl_parser.c:', YAJL + 'yajl_lex.c:', IJSON_EXT + 'items_basecoro.c:')


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
        raise RuntimeError('feedback is empty or outside ijson/yajl source')
    for required in REQUIRED:
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required[len(PREFIX):-1]} has no feedback')
    return features, tuples


def main() -> None:
    manifest = json.loads((PROJECT / 'manifest.json').read_text())
    base = json.loads((PROJECT / 'verification.json').read_text())
    overlay = json.loads((OVERLAY / 'verification.json').read_text())
    if overlay['base_image_id'] != base['image_id']:
        raise RuntimeError('AFL overlay base differs from verified project')
    if overlay['base_project_receipt_sha256'] != sha256((PROJECT / 'verification.json').read_bytes()).hexdigest():
        raise RuntimeError('AFL overlay was built from a different project receipt')
    control = ROOT / manifest['control']
    variant = ROOT / manifest['differential_control']
    for source, digest in ((control, manifest['control_sha256']),
                           (variant, manifest['differential_control_sha256'])):
        if sha256(source.read_bytes()).hexdigest() != digest:
            raise RuntimeError('valid control hash changed')
    with tempfile.TemporaryDirectory(prefix='parsarium-ijson-feedback-') as temporary:
        scratch = Path(temporary)
        outputs = {}
        for name, source in (('control', control), ('variant', variant)):
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
        if outputs['control'] != manifest['expected_output']:
            raise RuntimeError(f'valid object structure changed: {outputs["control"]}')
        if outputs['variant'] != manifest['differential_expected_output']:
            raise RuntimeError(f'valid array structure changed: {outputs["variant"]}')
        backend = run([*sandbox(control, scratch), '--entrypoint', '/opt/venv/bin/python',
                       base['image_id'], '-c', 'import ijson; print(ijson.backend_name)']).strip()
        if backend != 'yajl2_c':
            raise RuntimeError(f'default backend is {backend}, not yajl2_c')
        first = probe(overlay['image_id'], control, scratch, 'first')
        repeat = probe(overlay['image_id'], control, scratch, 'repeat')
        other = probe(overlay['image_id'], variant, scratch, 'other')
        other_repeat = probe(overlay['image_id'], variant, scratch, 'other-repeat')
    if first != repeat or other != other_repeat:
        raise RuntimeError('repeated ijson/yajl source feedback is unstable')
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    if feature_diff == 0 or tuple_diff == 0:
        raise RuntimeError('ijson/AFL feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    yajl_diff = len({value for value in first[0] ^ other[0] if value.startswith(YAJL)})
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'json/python/ijson', 'pass': True,
              'input_kind': 'two fixed valid RFC 8259 JSON controls',
              'tested_backend': backend,
              'feedback_scope': 'native ijson 3.6.0 _yajl2 C sources and embedded yajl 2.1.1 (rtobar fork) lexer/parser source regions',
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'control_repeat_identical': True, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_yajl_features': sum(value.startswith(YAJL) for value in first[0]),
              'variant_yajl_features': sum(value.startswith(YAJL) for value in other[0]),
              'parser_feature_difference': feature_diff,
              'yajl_feature_difference': yajl_diff,
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
