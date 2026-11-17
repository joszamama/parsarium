"""Check a Python YAML path against the hand-written typed trees and its parser AFL++ feedback.

Usage: python3 scripts/verify_python_yaml_feedback.py SLUG (a key of TARGETS)

The oracle is the hand-written EXPECTED tree in controls/yaml/check_controls.py
(cross-checked there with Ruby Psych when Ruby is on PATH). Every input mode
(bytes, decoded str, local binary stream) must give that exact tree. Each
valid control then runs REPEATS times through the Python line bridge (or the
LLVM region bridge for C-extension routes) and afl-showmap; repeats must be
identical and the two controls must differ in the scanner/parser sources the
target names and in AFL++ tuples. Wrapper targets also report the features of
their own package, which may be identical on both controls.
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
PY_DIFF = {'scanner_py_feature_difference': 'scanner.py:', 'parser_py_feature_difference': 'parser.py:'}
C_DIFF = {'scanner_c_feature_difference': 'scanner.c:', 'parser_c_feature_difference': 'parser.c:'}
PY_SCOPE = 'executed Python source lines of the installed {package} {release} package under {prefix}'
TARGETS = {
    'pyyaml': {'package': 'PyYAML', 'prefix': SITE + 'yaml/', 'platform': 'linux/amd64',
               'required': ('scanner.py', 'parser.py'), 'differences': PY_DIFF, 'scope': PY_SCOPE},
    'ruamel_yaml': {'package': 'ruamel.yaml', 'prefix': SITE + 'ruamel/yaml/', 'platform': 'linux/amd64',
                    'required': ('scanner.py', 'parser.py'), 'differences': PY_DIFF, 'scope': PY_SCOPE},
    'pyyaml_csafeloader': {
        'package': 'PyYAML CSafeLoader (libyaml)', 'prefix': '/work/libyaml-src/src/', 'platform': 'linux/arm64',
        'required': ('scanner.c', 'parser.c'), 'differences': C_DIFF,
        'scope': ('executed LLVM source regions and branch directions of the source-built libyaml 0.2.5 under '
                  '{prefix}, statically linked into the PyYAML {release} _yaml extension')},
    'ruamel_yaml_clib': {
        'package': 'ruamel.yaml.clib', 'prefix': '/work/clib-src/', 'platform': 'linux/arm64',
        'required': ('scanner.c', 'parser.c'), 'differences': C_DIFF,
        'scope': ('executed LLVM source regions and branch directions of the source-built {package} {release} '
                  'extension\'s libyaml-derived C sources under {prefix} (the Cython-generated _ruamel_yaml.c is '
                  'not instrumented)')},
    'rapidyaml': {
        'package': 'rapidyaml', 'prefix': '/work/ryml-src/cpp/src/c4/yml/', 'platform': 'linux/arm64',
        'required': ('parse_engine.def.hpp', 'tree.cpp'),
        'differences': {'parse_engine_feature_difference': 'parse_engine.def.hpp:',
                        'tree_feature_difference': 'tree.cpp:'},
        'scope': ('executed LLVM source regions and branch directions of the C++ rapidyaml {release} sources under '
                  '{prefix} compiled into the {package} _ryml extension (c4core helpers, the SWIG wrapper and the '
                  'adapter\'s Python scalar typing are not counted)')},
    'ryaml': {
        'package': 'ryaml',
        'prefix': '/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/unsafe-libyaml-0.2.11/src/',
        'platform': 'linux/arm64',
        'required': ('scanner.rs', 'parser.rs'),
        'differences': {'scanner_rs_feature_difference': 'scanner.rs:', 'parser_rs_feature_difference': 'parser.rs:'},
        'scope': ('executed LLVM source regions and branch directions of unsafe-libyaml 0.2.11 under {prefix}, compiled '
                  'into the source-built {package} {release} _ryaml extension (serde_yaml, pythonize and the PyO3 module '
                  'are not counted)')},
    'yaml_rs': {
        'package': 'yaml-rs',
        'prefix': '/usr/local/cargo/git/checkouts/granit-parser-adcc536166983974/e10ee63/src/',
        'platform': 'linux/arm64',
        'required': ('scanner.rs', 'parser.rs'),
        'differences': {'scanner_rs_feature_difference': 'scanner.rs:', 'parser_rs_feature_difference': 'parser.rs:'},
        'scope': ('executed LLVM source regions and branch directions of granit-parser (git e10ee63) under {prefix}, '
                  'compiled into the source-built {package} {release} _yaml_rs extension (yaml-rs\'s own loader, pyo3, '
                  'saphyr and lexical-core are not counted)')},
    # Wrappers: features cover the wrapper package and the parser package it calls under site-packages.
    'srsly': {
        'package': 'srsly', 'prefix': SITE, 'platform': 'linux/amd64',
        'required': ('srsly/_yaml_api.py', 'ruamel/yaml/scanner.py', 'ruamel/yaml/parser.py'),
        'packages': ('srsly/', 'ruamel/yaml/'),
        'differences': {'own_package_feature_difference': 'srsly/',
                        'ruamel_scanner_py_feature_difference': 'ruamel/yaml/scanner.py:',
                        'ruamel_parser_py_feature_difference': 'ruamel/yaml/parser.py:'},
        'scope': ('executed Python source lines of srsly {release} (wrapper) and of ruamel.yaml 0.19.1 (the parser '
                  'it calls) under {prefix}')},
    'yamlcore': {
        'package': 'yamlcore', 'prefix': SITE, 'platform': 'linux/amd64',
        'required': ('yamlcore/loader.py', 'yaml/scanner.py', 'yaml/parser.py'),
        'packages': ('yamlcore/', 'yaml/'),
        'differences': {'own_package_feature_difference': 'yamlcore/',
                        'pyyaml_scanner_py_feature_difference': 'yaml/scanner.py:',
                        'pyyaml_parser_py_feature_difference': 'yaml/parser.py:'},
        'scope': ('executed Python source lines of yamlcore {release} (resolver/constructor wrapper) and of PyYAML '
                  '6.0.3 (the pure-Python loader it extends) under {prefix}')},
}
REPEATS = 3
_spec = importlib.util.spec_from_file_location('yaml_check_controls', ROOT / 'controls/yaml/check_controls.py')
ORACLE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ORACLE)


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=300)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(source: Path, scratch: Path, platform: str) -> list[str]:
    return ['docker', 'run', '--rm', '--platform', platform, '--network', 'none',
            '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--user', f'{os.getuid()}:{os.getgid()}', '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
            '-v', f'{source}:/input/case:ro', '-v', f'{scratch}:/coverage']


def oracle(image: str, source: Path, scratch: Path, platform: str) -> dict:
    expected = ORACLE.EXPECTED[source.name]
    base = [*sandbox(source, scratch, platform), '--entrypoint', '/opt/venv/bin/python', image, '/work/structure.py']
    modes = {}
    for mode in ('bytes', 'str', 'stream'):
        observed = json.loads(run([*base, mode, '/input/case']))
        if observed['tree'] != expected:
            raise RuntimeError(f'{mode} tree differs from the hand-written oracle for {source.name}')
        modes[mode] = True
    return {'tree_sha256': ORACLE.tree_sha256(expected), **ORACLE.summary(expected),
            'bytes_matches_oracle': modes['bytes'], 'str_matches_oracle': modes['str'],
            'stream_matches_oracle': modes['stream']}


def probe(image: str, source: Path, scratch: Path, label: str, target: dict) -> tuple[set[str], set[str]]:
    prefix = target['prefix']
    base = sandbox(source, scratch, target['platform'])
    run([*base, '--entrypoint', '/bin/sh', image, '/work/afl_trace', '/input/case', f'/coverage/{label}.features'])
    run([*base, '-e', 'AFL_MAP_SIZE=65536', '--entrypoint', 'afl-showmap', image,
         '-m', 'none', '-t', '120000', '-o', f'/coverage/{label}.map', '--', '/work/afl_proxy', '/input/case'])
    features = set((scratch / f'{label}.features').read_text().splitlines()) - {''}
    tuples = {line.split(':', 1)[0] for line in (scratch / f'{label}.map').read_text().splitlines() if line}
    allowed = tuple(prefix + name for name in target.get('packages', ('',)))
    if not features or not tuples or any(not value.startswith(allowed) for value in features):
        raise RuntimeError('feedback is empty or outside the package source')
    for required in target['required']:
        if not any(value.startswith(prefix + required + ':') for value in features):
            raise RuntimeError(f'{required} has no feedback')
    return features, tuples


def by_file(features: set[str], prefix: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in features:
        name = value[len(prefix):].split(':', 1)[0]
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
    if manifest['platform'] != target['platform']:
        raise RuntimeError('manifest platform differs from the feedback target')
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
            outputs[name] = json.loads(run([*sandbox(source, scratch, target['platform']), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'], '/work/replay.py',
                                            '/input/case']))
            oracles[name] = oracle(base['image_id'], source, scratch, target['platform'])
        if outputs['control'] != manifest['expected_output']:
            raise RuntimeError('primary control output changed')
        if outputs['variant'] != manifest['differential_expected_output']:
            raise RuntimeError('differential control output changed')
        firsts = [probe(overlay['image_id'], control, scratch, f'control-{i}', target) for i in range(REPEATS)]
        others = [probe(overlay['image_id'], variant, scratch, f'variant-{i}', target) for i in range(REPEATS)]
    if any(item != firsts[0] for item in firsts) or any(item != others[0] for item in others):
        raise RuntimeError('repeated parser source feedback is unstable')
    first, other = firsts[0], others[0]
    difference = first[0] ^ other[0]
    named = {key: sum(value.startswith(prefix + name) for value in difference)
             for key, name in target['differences'].items()}
    parser_named = [count for key, count in named.items() if key != 'own_package_feature_difference']
    tuple_diff = len(first[1] ^ other[1])
    if not difference or not tuple_diff or not any(parser_named):
        raise RuntimeError('parser/AFL feedback does not distinguish the valid controls')
    if len(first[0]) != overlay['parser_source_features'] or len(first[1]) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    bridge = ('LLVM region bridge' if 'afl_llvm_module_glob' in manifest else 'Python line bridge')
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'project': f'yaml/python/{slug}', 'package': target['package'], 'release': manifest['release'],
              'pass': True, 'input_kind': 'two fixed valid schema-neutral YAML 1.2 controls',
              'oracle': 'hand-written typed trees in controls/yaml/check_controls.py (EXPECTED); bytes, decoded str and local binary stream inputs all equal them',
              'control_oracle': oracles['control'], 'variant_oracle': oracles['variant'],
              'feedback_scope': (target['scope'].format(package=target['package'], release=manifest['release'],
                                                        prefix=prefix)
                                 + f', mapped to the AFL++ bitmap by the Parsarium {bridge}'),
              'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
              'overlay_receipt_sha256': sha256((overlay_dir / 'verification.json').read_bytes()).hexdigest(),
              'control_sha256': manifest['control_sha256'], 'variant_sha256': manifest['differential_control_sha256'],
              'control_output': outputs['control'], 'variant_output': outputs['variant'],
              'runs_per_control': REPEATS, 'control_repeat_identical': True, 'variant_repeat_identical': True,
              'control_parser_features': len(first[0]), 'variant_parser_features': len(other[0]),
              'control_features_by_file': by_file(first[0], prefix),
              'variant_features_by_file': by_file(other[0], prefix),
              'parser_feature_difference': len(difference),
              **named,
              'control_afl_tuples': len(first[1]), 'variant_afl_tuples': len(other[1]),
              'afl_tuple_difference': tuple_diff}
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({key: value for key, value in report.items() if 'output' not in key}, indent=2))


if __name__ == '__main__':
    main()
