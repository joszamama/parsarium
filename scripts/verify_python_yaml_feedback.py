"""Check a Python YAML path against the hand-written typed trees and its parser-line AFL++ feedback.

Usage: python3 scripts/verify_python_yaml_feedback.py pyyaml|ruamel_yaml

The oracle is the hand-written EXPECTED tree in controls/yaml/check_controls.py
(cross-checked there with Ruby Psych when Ruby is on PATH). Every input mode
(bytes, decoded str, local binary stream) must give that exact tree. Each
valid control then runs REPEATS times through the Python line bridge and
afl-showmap; repeats must be identical and the two controls must differ in
the package's own scanner/parser lines and in AFL++ tuples.
"""
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SITE = '/opt/venv/lib/python3.14/site-packages/'
TARGETS = {
    'pyyaml': {'package': 'PyYAML', 'prefix': SITE + 'yaml/'},
    'ruamel_yaml': {'package': 'ruamel.yaml', 'prefix': SITE + 'ruamel/yaml/'},
}
REPEATS = 3
_spec = importlib.util.spec_from_file_location('yaml_check_controls', ROOT / 'controls/yaml/check_controls.py')
ORACLE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ORACLE)


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(source: Path, scratch: Path) -> list[str]:
    return ['docker', 'run', '--rm', '--platform', 'linux/amd64', '--network', 'none',
            '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--user', f'{os.getuid()}:{os.getgid()}', '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
            '-v', f'{source}:/input/case:ro', '-v', f'{scratch}:/coverage']


def oracle(image: str, source: Path, scratch: Path) -> dict:
    expected = ORACLE.EXPECTED[source.name]
    base = [*sandbox(source, scratch), '--entrypoint', '/opt/venv/bin/python', image, '/work/structure.py']
    modes = {}
    for mode in ('bytes', 'str', 'stream'):
        observed = json.loads(run([*base, mode, '/input/case']))
        if observed['tree'] != expected:
            raise RuntimeError(f'{mode} tree differs from the hand-written oracle for {source.name}')
        modes[mode] = True
    return {'tree_sha256': ORACLE.tree_sha256(expected), **ORACLE.summary(expected),
            'bytes_matches_oracle': modes['bytes'], 'str_matches_oracle': modes['str'],
            'stream_matches_oracle': modes['stream']}


def probe(image: str, source: Path, scratch: Path, label: str, prefix: str) -> tuple[set[str], set[str]]:
    base = sandbox(source, scratch)
    run([*base, '--entrypoint', '/bin/sh', image, '/work/afl_trace', '/input/case', f'/coverage/{label}.features'])
    run([*base, '-e', 'AFL_MAP_SIZE=65536', '--entrypoint', 'afl-showmap', image,
         '-m', 'none', '-t', '120000', '-o', f'/coverage/{label}.map', '--', '/work/afl_proxy', '/input/case'])
    features = set((scratch / f'{label}.features').read_text().splitlines()) - {''}
    tuples = {line.split(':', 1)[0] for line in (scratch / f'{label}.map').read_text().splitlines() if line}
    if not features or not tuples or any(not value.startswith(prefix) for value in features):
        raise RuntimeError('feedback is empty or outside the package source')
    for required in ('scanner.py:', 'parser.py:'):
        if not any(value.startswith(prefix + required) for value in features):
            raise RuntimeError(f'{required[:-1]} has no feedback')
    return features, tuples


def by_file(features: set[str], prefix: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in features:
        name = value[len(prefix):].rsplit(':', 1)[0]
        counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items()))


def main() -> None:
    slug = sys.argv[1]
    target = TARGETS[slug]
    prefix = target['prefix']
    project = ROOT / 'projects/yaml/python' / slug
    overlay_dir = ROOT / 'fuzzing/afl-native/yaml/python' / slug
    report_path = ROOT / f'data/python/yaml/{slug}-valid-feedback.json'
    manifest = json.loads((project / 'manifest.json').read_text())
    base = json.loads((project / 'verification.json').read_text())
    overlay = json.loads((overlay_dir / 'verification.json').read_text())
    if overlay['base_image_id'] != base['image_id']:
        raise RuntimeError('AFL overlay base differs from verified project')
    if overlay['base_project_receipt_sha256'] != sha256((project / 'verification.json').read_bytes()).hexdigest():
        raise RuntimeError('AFL overlay was built from a different project receipt')
    control = ROOT / manifest['control']
    variant = ROOT / manifest['differential_control']
    for source, digest in ((control, manifest['control_sha256']), (variant, manifest['differential_control_sha256'])):
        if sha256(source.read_bytes()).hexdigest() != digest:
            raise RuntimeError('valid control hash changed')
    ORACLE.check()
    with tempfile.TemporaryDirectory(prefix=f'parsarium-yaml-{slug}-feedback-') as temporary:
        scratch = Path(temporary)
        outputs, oracles = {}, {}
        for name, source in (('control', control), ('variant', variant)):
            outputs[name] = json.loads(run([*sandbox(source, scratch), '--entrypoint', '/opt/venv/bin/python',
                                            base['image_id'], '/work/replay.py', '/input/case']))
            oracles[name] = oracle(base['image_id'], source, scratch)
        if outputs['control'] != manifest['expected_output']:
            raise RuntimeError('primary control output changed')
        if outputs['variant'] != manifest['differential_expected_output']:
            raise RuntimeError('differential control output changed')
        firsts = [probe(overlay['image_id'], control, scratch, f'control-{i}', prefix) for i in range(REPEATS)]
        others = [probe(overlay['image_id'], variant, scratch, f'variant-{i}', prefix) for i in range(REPEATS)]
    if any(item != firsts[0] for item in firsts) or any(item != others[0] for item in others):
        raise RuntimeError('repeated parser source feedback is unstable')
    first, other = firsts[0], others[0]
    difference = first[0] ^ other[0]
    scanner_diff = sum(value.startswith(prefix + 'scanner.py:') for value in difference)
    parser_diff = sum(value.startswith(prefix + 'parser.py:') for value in difference)
    tuple_diff = len(first[1] ^ other[1])
    if not difference or not tuple_diff or not (scanner_diff or parser_diff):
        raise RuntimeError('parser/AFL feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': f'yaml/python/{slug}', 'package': target['package'], 'release': manifest['release'],
              'pass': True, 'input_kind': 'two fixed valid schema-neutral YAML 1.2 controls',
              'oracle': 'hand-written typed trees in controls/yaml/check_controls.py (EXPECTED); bytes, decoded str and local binary stream inputs all equal them',
              'control_oracle': oracles['control'], 'variant_oracle': oracles['variant'],
              'feedback_scope': f'executed Python source lines of the installed {target["package"]} {manifest["release"]} package under {prefix}, mapped to the AFL++ bitmap by the Parsarium Python line bridge',
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((overlay_dir / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'], 'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'runs_per_control': REPEATS, 'control_repeat_identical': True, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_features_by_file': by_file(first[0], prefix),
              'variant_features_by_file': by_file(other[0], prefix),
              'parser_feature_difference': len(difference),
              'scanner_py_feature_difference': scanner_diff, 'parser_py_feature_difference': parser_diff,
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({key: value for key, value in report.items() if 'output' not in key}, indent=2))


if __name__ == '__main__':
    main()
