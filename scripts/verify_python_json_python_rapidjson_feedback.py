"""Check python-rapidjson structure against a CPython json oracle and its native source feedback on two valid controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/json/python/python-rapidjson'
OVERLAY = ROOT / 'fuzzing/afl-native/json/python/python-rapidjson'
REPORT = ROOT / 'data/python/json/python-rapidjson-valid-feedback.json'
PREFIX = '/work/rapidjson-source/'
WRAPPER = PREFIX + 'rapidjson.cpp:'
RAPIDJSON = PREFIX + 'rapidjson/include/rapidjson/'
READER = RAPIDJSON + 'reader.h:'
REQUIRED = (WRAPPER, READER)
UNUSED = tuple(RAPIDJSON + name + ':' for name in ('writer.h', 'prettywriter.h', 'schema.h', 'document.h'))
MODES = ('load-stream', 'loads-bytes', 'loads-str')


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


def object_keys(tree: list) -> int:
    kind = tree[0]
    if kind == 'object':
        return len(tree[1]) + sum(object_keys(value) for _, value in tree[1])
    if kind == 'array':
        return sum(object_keys(value) for value in tree[1])
    return 0


def kinds(tree: list, found: set[str]) -> set[str]:
    found.add(tree[0])
    if tree[0] == 'object':
        for _, value in tree[1]:
            kinds(value, found)
    elif tree[0] == 'array':
        for value in tree[1]:
            kinds(value, found)
    return found


def oracle(image: str, source: Path, scratch: Path) -> dict:
    """Exact type-tagged trees from rapidjson (stream, bytes, str) and from CPython json without rapidjson."""
    base = [*sandbox(source, scratch), '--entrypoint']
    runs = [(mode, '/opt/venv/bin/python', []) for mode in MODES] + [('stdlib', '/usr/bin/python3', ['-I'])]
    trees = {mode: json.loads(run([*base, python, image, *flags, '/work/structure.py', mode, '/input/case']))
             for mode, python, flags in runs}
    stdlib = trees['stdlib']
    if not (stdlib['json_c_scanner'] and stdlib['json_c_scanstring']):
        raise RuntimeError('CPython json oracle did not use its _json C scanner')
    for mode in MODES:
        if trees[mode]['tree'] != stdlib['tree']:
            raise RuntimeError(f'{mode} tree differs from the CPython json oracle')
    keys = object_keys(stdlib['tree'])
    if keys != stdlib['object_pairs']:
        raise RuntimeError('control contains duplicate object keys')
    return {'oracle_python': stdlib['python'], 'python_rapidjson': trees['load-stream']['rapidjson'],
            'rapidjson_exact_version': trees['load-stream']['rapidjson_exact_version'],
            'tree_sha256': sha256(json.dumps(stdlib['tree'], ensure_ascii=False,
                                             sort_keys=True).encode()).hexdigest(),
            'value_kinds': sorted(kinds(stdlib['tree'], set())),
            'object_members': keys, 'duplicate_keys': 0,
            'load_stream_matches_oracle': True, 'loads_bytes_matches_oracle': True,
            'loads_str_matches_oracle': True}


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
        raise RuntimeError('feedback is empty or outside python-rapidjson source')
    for required in REQUIRED:
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required[len(PREFIX):-1]} has no feedback')
    if any(value.startswith(UNUSED) for value in features):
        raise RuntimeError('writer, schema or DOM source appeared in load feedback')
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
    with tempfile.TemporaryDirectory(prefix='parsarium-python-rapidjson-feedback-') as temporary:
        scratch = Path(temporary)
        outputs = {}
        oracles = {}
        for name, source in (('control', control), ('variant', variant)):
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
            oracles[name] = oracle(base['image_id'], source, scratch)
        if outputs['control'] != manifest['expected_output']:
            raise RuntimeError(f'valid object structure changed: {outputs["control"]}')
        if outputs['variant'] != manifest['differential_expected_output']:
            raise RuntimeError(f'valid array structure changed: {outputs["variant"]}')
        first = probe(overlay['image_id'], control, scratch, 'first')
        repeat = probe(overlay['image_id'], control, scratch, 'repeat')
        other = probe(overlay['image_id'], variant, scratch, 'other')
        other_repeat = probe(overlay['image_id'], variant, scratch, 'other-repeat')
    if first != repeat or other != other_repeat:
        raise RuntimeError('repeated python-rapidjson source feedback is unstable')
    def count(features: set[str], prefix: str) -> int:
        return sum(value.startswith(prefix) for value in features)

    difference = first[0] ^ other[0]
    feature_diff = len(difference)
    tuple_diff = len(first[1] ^ other[1])
    reader_diff = count(difference, READER)
    if feature_diff == 0 or tuple_diff == 0 or reader_diff == 0:
        raise RuntimeError('RapidJSON reader/AFL feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'json/python/python-rapidjson', 'pass': True,
              'input_kind': 'two fixed valid RFC 8259 JSON controls',
              'oracle': 'CPython json.loads (with _json C scanner) under /usr/bin/python3 -I in the same image, where rapidjson is not importable; exact type-tagged trees with float.hex values and object member order',
              'control_oracle': oracles['control'], 'variant_oracle': oracles['variant'],
              'feedback_scope': 'native python-rapidjson 1.26 extension source regions and branches: wrapper rapidjson.cpp and vendored Tencent RapidJSON v1.1.0-763-g24b5e7a8 headers; CPython headers and interpreter code are excluded',
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'control_repeat_identical': True, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_rapidjson_features': count(first[0], RAPIDJSON),
              'variant_rapidjson_features': count(other[0], RAPIDJSON),
              'control_reader_h_features': count(first[0], READER),
              'variant_reader_h_features': count(other[0], READER),
              'control_wrapper_features': count(first[0], WRAPPER),
              'variant_wrapper_features': count(other[0], WRAPPER),
              'parser_feature_difference': feature_diff,
              'rapidjson_feature_difference': count(difference, RAPIDJSON),
              'reader_h_feature_difference': reader_diff,
              'wrapper_feature_difference': count(difference, WRAPPER),
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
