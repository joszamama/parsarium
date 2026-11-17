"""Check pysimdjson trees against a CPython json oracle and its native source feedback on two valid controls."""
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'projects/json/python/pysimdjson'
OVERLAY = ROOT / 'fuzzing/afl-native/json/python/pysimdjson'
REPORT = ROOT / 'data/python/json/pysimdjson-valid-feedback.json'
PREFIX = '/work/pysimdjson-source/simdjson/'
KERNEL = PREFIX + 'simdjson.cpp:'
HEADER = PREFIX + 'simdjson.h:'
UNDERLYING = (KERNEL, HEADER)
WRAPPER = (PREFIX + 'csimdjson.cpp:', PREFIX + 'util.cpp:', PREFIX + 'util.h:', PREFIX + 'ondemand.h:')
# Amalgamated simdjson.cpp sections (begin/end file markers) for the arm64.cpp and fallback.cpp kernels.
ARM64 = range(14137, 21856)
FALLBACK = range(74530, 79830)


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(source: Path, scratch: Path) -> list[str]:
    return ['docker', 'run', '--rm', '--platform', 'linux/arm64', '--network', 'none',
            '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--user', f'{os.getuid()}:{os.getgid()}', '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
            '-e', 'LLVM_PROFILE_FILE=/tmp/structure-%p.profraw',
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
    """Exact type-tagged trees from Parser.parse/Parser.load and from CPython json without pysimdjson."""
    base = [*sandbox(source, scratch), '--entrypoint']
    trees = {mode: json.loads(run([*base, python, image, *flags, '/work/structure.py', mode, '/input/case']))
             for mode, python, flags in (('pysimdjson-parse', '/opt/venv/bin/python', []),
                                         ('pysimdjson-load', '/opt/venv/bin/python', []),
                                         ('stdlib', '/usr/bin/python3', ['-I']))}
    stdlib = trees['stdlib']
    if not (stdlib['json_c_scanner'] and stdlib['json_c_scanstring']):
        raise RuntimeError('CPython json oracle did not use its _json C scanner')
    for mode in ('pysimdjson-parse', 'pysimdjson-load'):
        if trees[mode]['tree'] != stdlib['tree']:
            raise RuntimeError(f'{mode} tree differs from the CPython json oracle')
        if trees[mode]['implementation'][0] != 'arm64' or trees[mode]['simdjson'] != '5.1.1':
            raise RuntimeError(f'{mode} did not run the simdjson 5.1.1 arm64 kernel')
    keys = object_keys(stdlib['tree'])
    if keys != stdlib['object_pairs']:
        raise RuntimeError('control contains duplicate object keys')
    native = trees['pysimdjson-parse']
    return {'oracle_python': stdlib['python'], 'simdjson': native['simdjson'],
            'active_implementation': native['implementation'],
            'compiled_implementations': native['compiled_implementations'],
            'tree_sha256': sha256(json.dumps(stdlib['tree'], ensure_ascii=False,
                                             sort_keys=True).encode()).hexdigest(),
            'value_kinds': sorted(kinds(stdlib['tree'], set())),
            'object_members': keys, 'duplicate_keys': 0,
            'parse_bytes_matches_oracle': True, 'load_path_matches_oracle': True,
            'stdlib_decoding_disabled': True}


def line_of(feature: str) -> int:
    return int(feature[len(KERNEL):].split(':', 1)[0])


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
    if not features or not tuples or any(not value.startswith(UNDERLYING + WRAPPER) for value in features):
        raise RuntimeError('feedback is empty or outside pysimdjson/simdjson source')
    for required in (KERNEL, HEADER, WRAPPER[0]):
        if not any(value.startswith(required) for value in features):
            raise RuntimeError(f'{required[len(PREFIX):-1]} has no feedback')
    kernel = [line_of(value) for value in features if value.startswith(KERNEL)]
    if not any(line in ARM64 for line in kernel) or any(line in FALLBACK for line in kernel):
        raise RuntimeError('feedback did not come from the arm64 kernel alone')
    return features, tuples


def count(features: set[str], prefixes: tuple[str, ...]) -> int:
    return sum(value.startswith(prefixes) for value in features)


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
    with tempfile.TemporaryDirectory(prefix='parsarium-pysimdjson-feedback-') as temporary:
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
        raise RuntimeError('repeated pysimdjson source feedback is unstable')
    difference = first[0] ^ other[0]
    feature_diff = len(difference)
    tuple_diff = len(first[1] ^ other[1])
    underlying_diff = count(difference, UNDERLYING)
    wrapper_diff = count(difference, WRAPPER)
    # Both controls reach every Cython conversion branch, so the input-dependent part is simdjson's.
    if feature_diff == 0 or tuple_diff == 0 or underlying_diff == 0:
        raise RuntimeError('pysimdjson/AFL feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    arm64_diff = sum(line_of(value) in ARM64 for value in difference if value.startswith(KERNEL))
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': 'json/python/pysimdjson', 'pass': True,
              'input_kind': 'two fixed valid RFC 8259 JSON controls',
              'api': 'simdjson.Parser().parse(bytes, recursive=True) and Parser().load(path, recursive=True)',
              'oracle': 'CPython json.loads (with _json C scanner) under /usr/bin/python3 -I in the same image, where pysimdjson is not importable; exact type-tagged trees with float.hex values and object member order. In the pysimdjson runs, stdlib json decoding entry points are replaced with a hard failure before import.',
              'control_oracle': oracles['control'], 'variant_oracle': oracles['variant'],
              'feedback_scope': 'native csimdjson extension source regions and branches, split into the pysimdjson 8.0.0 wrapper (Cython-generated csimdjson.cpp, util.cpp) and vendored simdjson 5.1.1 (simdjson.cpp, simdjson.h); CPython headers excluded',
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'],
              'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'control_repeat_identical': True, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_wrapper_features': count(first[0], WRAPPER),
              'variant_wrapper_features': count(other[0], WRAPPER),
              'control_simdjson_features': count(first[0], UNDERLYING),
              'variant_simdjson_features': count(other[0], UNDERLYING),
              'control_arm64_kernel_features': sum(line_of(v) in ARM64 for v in first[0] if v.startswith(KERNEL)),
              'variant_arm64_kernel_features': sum(line_of(v) in ARM64 for v in other[0] if v.startswith(KERNEL)),
              'fallback_kernel_features': 0,
              'parser_feature_difference': feature_diff,
              'wrapper_feature_difference': wrapper_diff,
              'simdjson_feature_difference': underlying_diff,
              'arm64_kernel_feature_difference': arm64_diff,
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
