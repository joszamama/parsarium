"""Check a Python TOML path's typed trees and its parser-source AFL++ feedback on the two valid TOML controls.

Usage: python3 scripts/verify_python_toml_feedback.py SLUG (a key of PACKAGES)

Every API mode of the package, and CPython tomllib run where the package is not
importable, must give the hand-written typed tree of each control. The AFL++ overlay
must then give identical, parser-scoped feedback on three runs per control, and the
two controls must differ by at least two source features and two AFL++ tuples.
Pure-Python packages use the Python line bridge; native extensions (``native``
targets) use the LLVM region bridge over the compiled parser sources named by the
manifest's afl_coverage_subject_prefix.
"""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPEATS = 3
PACKAGES = {
    "tomlkit": {"modes": ("tomlkit-items", "tomlkit-unwrap", "tomlkit-bytes", "tomlkit-stream"),
                "parser_file": "parser.py",
                "stdlib_family": "independent (tomllib is the tomli family)"},
    "tomli": {"modes": ("tomli-str", "tomli-stream"),
              "parser_file": "_parser.py",
              "stdlib_family": "same family (tomllib is a vendored copy of tomli); hand-written trees are the independent check"},
    "rtoml": {"modes": ("rtoml-str", "rtoml-path", "rtoml-stream"),
              "parser_file": "_parser-1.1.5+spec-1.1.0/src/parser/document.rs",
              "stdlib_family": "independent (tomllib is the tomli family; rtoml is the Rust toml_parser family)",
              "native": ("executed LLVM source regions and branch directions of the toml 1.1.8, toml_parser 1.1.5 "
                         "and toml_datetime 1.1.2 crate sources under {prefix}, compiled into the source-built "
                         "rtoml {release} _rtoml extension")},
}


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=600)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(platform: str, source: Path, scratch: Path) -> list[str]:
    return ['docker', 'run', '--rm', '--platform', platform, '--network', 'none',
            '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--user', f'{os.getuid()}:{os.getgid()}', '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
            '-v', f'{source}:/input/case:ro', '-v', f'{scratch}:/coverage']


def canonical_sha(tree) -> str:
    return sha256(json.dumps(tree, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def oracle(slug: str, platform: str, image: str, source: Path, expected, scratch: Path) -> dict:
    base = [*sandbox(platform, source, scratch), '--entrypoint']
    reports = {}
    for mode in PACKAGES[slug]["modes"]:
        reports[mode] = json.loads(run([*base, '/opt/venv/bin/python', image,
                                        '/work/structure.py', mode, '/input/case']))
    reports['stdlib'] = json.loads(run([*base, '/usr/bin/python3', image, '-I',
                                        '/work/structure.py', 'stdlib', '/input/case']))
    for mode, report in reports.items():
        if report['tree'] != expected:
            raise RuntimeError(f'{mode} typed tree differs from the hand-written expected tree')
    return {'modes_matching_expected_tree': list(PACKAGES[slug]["modes"]),
            'stdlib_tomllib_python': reports['stdlib']['python'],
            'stdlib_tomllib_matches': True,
            'stdlib_tomllib_family': PACKAGES[slug]["stdlib_family"],
            'package_version': reports[PACKAGES[slug]["modes"][0]][slug],
            'tree_sha256': canonical_sha(expected)}


def probe(platform: str, image: str, prefix: str, parser_file: str,
          source: Path, scratch: Path, label: str) -> tuple[frozenset, frozenset]:
    base = sandbox(platform, source, scratch)
    run([*base, '--entrypoint', '/bin/sh', image,
         '/work/afl_trace', '/input/case', f'/coverage/{label}.features'])
    run([*base, '-e', 'AFL_MAP_SIZE=65536', '--entrypoint', 'afl-showmap', image,
         '-m', 'none', '-t', '120000', '-o', f'/coverage/{label}.map',
         '--', '/work/afl_proxy', '/input/case'])
    features = frozenset((scratch / f'{label}.features').read_text().splitlines()) - {''}
    tuples = frozenset(line.split(':', 1)[0] for line in
                       (scratch / f'{label}.map').read_text().splitlines() if line)
    if not features or not tuples or any(not value.startswith(prefix) for value in features):
        raise RuntimeError('feedback is empty or outside the package source')
    if not any(value.startswith(prefix + parser_file + ':') for value in features):
        raise RuntimeError(f'{parser_file} has no feedback')
    return features, tuples


def per_file(prefix: str, features) -> dict:
    # Python line features are file:line; native region features are file:line:column[:branch].
    return dict(sorted(Counter(value[len(prefix):].split(':', 1)[0] for value in features).items()))


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in PACKAGES:
        raise SystemExit(__doc__)
    slug = sys.argv[1]
    project = ROOT / 'projects/toml/python' / slug
    overlay_dir = ROOT / 'fuzzing/afl-native/toml/python' / slug
    manifest = json.loads((project / 'manifest.json').read_text())
    base = json.loads((project / 'verification.json').read_text())
    overlay = json.loads((overlay_dir / 'verification.json').read_text())
    platform = manifest['platform']
    prefix = manifest.get('afl_coverage_subject_prefix', manifest['coverage_subject_prefix'])
    parser_file = PACKAGES[slug]['parser_file']
    if overlay['base_image_id'] != base['image_id']:
        raise RuntimeError('AFL overlay base differs from verified project')
    if overlay['base_project_receipt_sha256'] != sha256((project / 'verification.json').read_bytes()).hexdigest():
        raise RuntimeError('AFL overlay was built from a different project receipt')
    control = ROOT / manifest['control']
    variant = ROOT / manifest['differential_control']
    for source, digest in ((control, manifest['control_sha256']),
                           (variant, manifest['differential_control_sha256'])):
        if sha256(source.read_bytes()).hexdigest() != digest:
            raise RuntimeError('valid control hash changed')
    expected = {'control': json.loads(control.with_name(control.stem + '.expected.json').read_text()),
                'variant': json.loads(variant.with_name(variant.stem + '.expected.json').read_text())}
    if (expected['control'] != manifest['expected_output'] or
            expected['variant'] != manifest['differential_expected_output']):
        raise RuntimeError('manifest trees differ from the committed expected trees')
    with tempfile.TemporaryDirectory(prefix=f'parsarium-toml-{slug}-feedback-') as temporary:
        scratch = Path(temporary)
        outputs, oracles = {}, {}
        for name, source in (('control', control), ('variant', variant)):
            outputs[name] = json.loads(run([*sandbox(platform, source, scratch), '--entrypoint',
                                            '/opt/venv/bin/python', base['image_id'],
                                            '/work/replay.py', '/input/case']))
            if outputs[name] != expected[name]:
                raise RuntimeError(f'{name} typed tree changed')
            oracles[name] = oracle(slug, platform, base['image_id'], source, expected[name], scratch)
        firsts = [probe(platform, overlay['image_id'], prefix, parser_file, control, scratch, f'control-{i}')
                  for i in range(REPEATS)]
        others = [probe(platform, overlay['image_id'], prefix, parser_file, variant, scratch, f'variant-{i}')
                  for i in range(REPEATS)]
    if any(item != firsts[0] for item in firsts) or any(item != others[0] for item in others):
        raise RuntimeError(f'repeated {slug} source feedback is unstable')
    (first, first_tuples), (other, other_tuples) = firsts[0], others[0]
    parser_prefix = prefix + parser_file + ':'
    feature_diff = len(first ^ other)
    tuple_diff = len(first_tuples ^ other_tuples)
    parser_diff = len({value for value in first ^ other if value.startswith(parser_prefix)})
    if feature_diff < 2 or tuple_diff < 2 or parser_diff == 0:
        raise RuntimeError(f'{slug}/AFL feedback does not distinguish the valid controls')
    if len(first) != overlay['parser_source_features'] or len(first_tuples) != overlay['feedback_edges']:
        raise RuntimeError('control feedback differs from overlay receipt')
    report = {
        'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'project': f'toml/python/{slug}', 'pass': True,
        'input_kind': 'two fixed valid TOML 1.0.0 controls',
        'oracle': 'hand-written typed trees in controls/toml/*.expected.json; every package API mode and CPython tomllib (/usr/bin/python3 -I in the same image, where the package is not importable) must equal them',
        'control_oracle': oracles['control'], 'variant_oracle': oracles['variant'],
        'feedback_scope': (
            PACKAGES[slug]['native'].format(prefix=prefix, release=manifest['release'])
            + ', mapped to the AFL++ bitmap by the Parsarium LLVM region bridge'
            if 'native' in PACKAGES[slug] else
            f'executed Python source lines of the installed {slug} {manifest["release"]} package under {prefix}, mapped to the AFL++ bitmap by the Parsarium Python line bridge'),
        'base_image_id': base['image_id'], 'overlay_image_id': overlay['image_id'],
        'overlay_receipt_sha256': sha256((overlay_dir / 'verification.json').read_bytes()).hexdigest(),
        'control': manifest['control'], 'control_sha256': manifest['control_sha256'],
        'variant': manifest['differential_control'], 'variant_sha256': manifest['differential_control_sha256'],
        'control_output_sha256': canonical_sha(outputs['control']),
        'variant_output_sha256': canonical_sha(outputs['variant']),
        'runs_per_control': REPEATS,
        'control_repeat_identical': True, 'variant_repeat_identical': True,
        'control_parser_features': len(first), 'variant_parser_features': len(other),
        'control_parser_lines_per_file': per_file(prefix[:prefix.rfind('/') + 1], first),
        'variant_parser_lines_per_file': per_file(prefix[:prefix.rfind('/') + 1], other),
        'format_parser_file': parser_file,
        'control_format_parser_features': sum(value.startswith(parser_prefix) for value in first),
        'variant_format_parser_features': sum(value.startswith(parser_prefix) for value in other),
        'control_only_features': len(first - other), 'variant_only_features': len(other - first),
        'parser_feature_difference': feature_diff,
        'format_parser_feature_difference': parser_diff,
        'control_afl_tuples': len(first_tuples), 'variant_afl_tuples': len(other_tuples),
        'control_only_afl_tuples': len(first_tuples - other_tuples),
        'variant_only_afl_tuples': len(other_tuples - first_tuples),
        'afl_tuple_difference': tuple_diff,
    }
    out = ROOT / 'data/python/toml' / f'{slug}-valid-feedback.json'
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
