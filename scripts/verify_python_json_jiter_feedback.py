"""Check jiter.from_json trees against a CPython json oracle and its native Jiter feedback on two valid controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/json/python/jiter'
OVERLAY = ROOT / 'fuzzing/afl-native/json/python/jiter'
REPORT = ROOT / 'data/python/json/jiter-valid-feedback.json'
PREFIX = '/work/jiter-source/crates/jiter/src/'
PARSE = PREFIX + 'parse.rs:'
REQUIRED = tuple(PREFIX + name + ':' for name in
                 ('parse.rs', 'python.rs', 'string_decoder.rs', 'number_decoder.rs'))
# The Python path builds objects in python.rs; JsonValue and the Jiter iterator API stay idle.
UNUSED = tuple(PREFIX + name + ':' for name in ('value.rs', 'jiter.rs'))


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
    """Exact type-tagged trees from jiter and from CPython json without jiter."""
    base = [*sandbox(source, scratch), '--entrypoint']
    trees = {mode: json.loads(run([*base, python, image, *flags, '/work/structure.py', mode, '/input/case']))
             for mode, python, flags in (('jiter', '/opt/venv/bin/python', []),
                                         ('stdlib', '/usr/bin/python3', ['-I']))}
    stdlib = trees['stdlib']
    if not (stdlib['json_c_scanner'] and stdlib['json_c_scanstring']):
        raise RuntimeError('CPython json oracle did not use its _json C scanner')
    if trees['jiter']['tree'] != stdlib['tree']:
        raise RuntimeError('jiter tree differs from the CPython json oracle')
    keys = object_keys(stdlib['tree'])
    if keys != stdlib['object_pairs']:
        raise RuntimeError('control contains duplicate object keys')
    return {'oracle_python': stdlib['python'], 'jiter': trees['jiter']['jiter'],
            'tree_sha256': sha256(json.dumps(stdlib['tree'], ensure_ascii=False,
                                             sort_keys=True).encode()).hexdigest(),
            'value_kinds': sorted(kinds(stdlib['tree'], set())),
            'object_members': keys, 'duplicate_keys': 0, 'bytes_matches_oracle': True}


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
        raise RuntimeError('feedback is empty or outside the Jiter crate source')
    for required in REQUIRED:
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required[len(PREFIX):-1]} has no feedback')
    if any(value.startswith(UNUSED) for value in features):
        raise RuntimeError('JsonValue or iterator source appeared in from_json feedback')
    return features, tuples


def count(features: set[str], prefix: str) -> int:
    return sum(value.startswith(prefix) for value in features)


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
    with tempfile.TemporaryDirectory(prefix='parsarium-jiter-feedback-') as temporary:
        scratch = Path(temporary)
        outputs = {}
        oracles = {}
        for name, source in (('control', control), ('variant', variant)):
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
            oracles[name] = oracle(base['image_id'], source, scratch)
        if outputs['control'] != manifest['expected_output']:
            raise RuntimeError(f'nested-object summary changed: {outputs["control"]}')
        if outputs['variant'] != manifest['differential_expected_output']:
            raise RuntimeError(f'nested-array summary changed: {outputs["variant"]}')
        first = probe(overlay['image_id'], control, scratch, 'first')
        repeat = probe(overlay['image_id'], control, scratch, 'repeat')
        other = probe(overlay['image_id'], variant, scratch, 'other')
        other_repeat = probe(overlay['image_id'], variant, scratch, 'other-repeat')
    if first != repeat or other != other_repeat:
        raise RuntimeError('repeated Jiter source feedback is unstable')
    feature_diff = len(first[0] ^ other[0])
    tuple_diff = len(first[1] ^ other[1])
    parse_diff = count(first[0] ^ other[0], PARSE)
    if feature_diff == 0 or tuple_diff == 0 or parse_diff == 0:
        raise RuntimeError('Jiter/AFL feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    differing = sorted({value[len(PREFIX):].split(':', 1)[0] for value in first[0] ^ other[0]})
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'json/python/jiter', 'pass': True,
              'input_kind': 'two fixed valid RFC 8259 JSON controls',
              'oracle': 'CPython json.loads (with _json C scanner) under /usr/bin/python3 -I in the same image, where jiter is not importable; exact type-tagged trees with float.hex values and object member order',
              'expected_summaries': 'hand-written from the control text in manifest.json; replay output must equal them',
              'control_oracle': oracles['control'], 'variant_oracle': oracles['variant'],
              'feedback_scope': 'native Jiter 0.19.0 Rust crate source regions and branches (crates/jiter/src) in the source-built jiter extension; PyO3 module wrapper and lexical-parse-float are outside AFL feedback',
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'control_repeat_identical': True, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_parse_rs_features': count(first[0], PARSE),
              'variant_parse_rs_features': count(other[0], PARSE),
              'value_rs_or_jiter_rs_features': 0,
              'parser_feature_difference': feature_diff,
              'parse_rs_feature_difference': parse_diff,
              'differing_source_files': differing,
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
