"""Build the tagged StereoKit C path with AFL++ feedback scoped to model_ply.cpp.

Only fixed valid ASCII PLY examples are replayed; this does not run a campaign.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
RELATIVE = OVERLAY.relative_to(ROOT / 'fuzzing/afl-native')
PROJECT = ROOT / 'projects' / RELATIVE
MANIFEST = json.loads((PROJECT / 'manifest.json').read_text())
sys.path.insert(0, str(ROOT / 'scripts'))
from docker_slots import docker_build_slot

IMAGE = 'parsarium-afl/ascii_ply-c-stereokit:local'
AFL_RELEASE = '4.33c-1.1ubuntu1'
SANDBOX = ['--network', 'none', '--read-only', '--cap-drop', 'ALL',
           '--security-opt', 'no-new-privileges', '--user', f'{os.getuid()}:{os.getgid()}',
           '--tmpfs', '/tmp:rw,exec,nosuid,size=64m', '--workdir', '/tmp']


def call(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'{command[:6]} failed: {(result.stdout + result.stderr)[-3500:]}')
    return result.stdout.strip()


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def image_run(*args: str) -> str:
    return call(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                 *SANDBOX, *args])


def replay(path: Path) -> dict:
    return json.loads(image_run('-v', f'{path}:/input/control:ro',
                                '--entrypoint', '/work/replay', IMAGE, '/input/control'))


def edge_ids(path: Path, map_size: int, directory: Path, label: str) -> set[str]:
    output = directory / f'{label}.map'
    probe = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                            *SANDBOX, '-e', f'AFL_MAP_SIZE={map_size}',
                            '-v', f'{path}:/input/control:ro',
                            '-v', f'{directory}:/coverage', '--entrypoint', 'afl-showmap',
                            IMAGE, '-e', '-m', 'none', '-t', '30000',
                            '-o', f'/coverage/{label}.map', '--',
                            '/work/replay', '/input/control'],
                           cwd=ROOT, capture_output=True, text=True)
    report = probe.stdout + probe.stderr
    if (probe.returncode or not re.search(r'Captured \d+ tuples', report)
            or f'map size {map_size}' not in report):
        raise RuntimeError(f'afl-showmap {label}: {report[-3500:]}')
    ids = {line.partition(':')[0] for line in output.read_text().splitlines() if line}
    output.unlink()
    return ids


def main() -> None:
    base = PROJECT / 'verification.json'
    if not base.is_file() or json.loads(base.read_text()).get('pass') is not True:
        raise RuntimeError('verified StereoKit C control is required')
    dockerfile = OVERLAY / 'Dockerfile'
    shutil.copyfile(PROJECT / 'Dockerfile', dockerfile)
    with docker_build_slot():
        call(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
              '--build-arg', 'PARSARIUM_BUILD=afl', '-f', str(dockerfile),
              '-t', IMAGE, str(PROJECT)])
    image_id = call(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = image_run('--entrypoint', 'dpkg-query', IMAGE, '-W', '-f=${Version}', 'afl++')
    if version != AFL_RELEASE:
        raise RuntimeError(f'AFL++ version mismatch: {version}')
    control = ROOT / MANIFEST['control']
    variant = OVERLAY / 'valid-quad.ply'
    observed = replay(control)
    if observed != MANIFEST['expected_output']:
        raise RuntimeError(f'AFL control changed: {observed}')
    variant_observed = replay(variant)
    if variant_observed['vertices'] != 4 or variant_observed['indices'] != 6:
        raise RuntimeError(f'valid quad not triangulated: {variant_observed}')
    # The selected source allowlist leaves the executable itself without AFL
    # sites, so AFL_DUMP_MAP_SIZE does not run before replay's argc check.
    # `afl-showmap` confirms its 64 KiB map in every fixed-control replay.
    map_size = 65536
    with tempfile.TemporaryDirectory(prefix='parsarium-stereokit-afl-') as temporary:
        directory = Path(temporary)
        controls = [edge_ids(control, map_size, directory, f'control-{i}') for i in range(3)]
        variants = [edge_ids(variant, map_size, directory, f'variant-{i}') for i in range(2)]
    control_stable = set.intersection(*controls)
    control_union = set.union(*controls)
    variant_stable = set.intersection(*variants)
    ratio = len(control_stable) / len(control_union) if control_union else 0
    if len(control_stable) < 2 or ratio < 0.99 or not (variant_stable - control_union):
        raise RuntimeError(f'PLY parser map lacks stable differential feedback: '
                           f'{len(control_stable)}/{len(control_union)}, '
                           f'{len(variant_stable - control_union)} variant-only')
    feedback = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_scope': 'AFL++ CLASSIC source allowlist src:model_ply.cpp, including bundled micro_ply implementation',
        'afl_map_size': map_size, 'control_sha256': digest(control),
        'valid_variant': str(variant.relative_to(ROOT)), 'valid_variant_sha256': digest(variant),
        'control_repeat_edge_counts': [len(edges) for edges in controls],
        'control_stable_edge_ids': len(control_stable),
        'control_union_edge_ids': len(control_union),
        'control_stability_ratio': round(ratio, 6),
        'variant_repeat_edge_counts': [len(edges) for edges in variants],
        'variant_stable_edge_ids': len(variant_stable),
        'stable_variant_only_edge_ids': len(variant_stable - control_union),
        'control_output': observed, 'variant_output': variant_observed,
        'mutation_campaign_run': False,
    }
    feedback_file = OVERLAY / 'feedback-validation.json'
    feedback_file.write_text(json.dumps(feedback, indent=2) + '\n')
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'stereokit_micro_ply_source_scoped_afl_edges',
        'feedback_scope': feedback['feedback_scope'],
        'base_project_receipt_sha256': digest(base),
        'source_sha256': MANIFEST['source_sha256'],
        'control_sha256': MANIFEST['control_sha256'],
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version, 'afl_version_output': version,
        'afl_map_size': map_size, 'afl_entrypoint': '/work/replay',
        'afl_file_input': True, 'feedback_edges': len(controls[0]),
        'overlay_file_sha256': {name: digest(OVERLAY / name)
                                for name in ('Dockerfile', 'build.py', 'valid-quad.ply',
                                             'feedback-validation.json')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(controls[0])} AFL++ parser edges; '
          f'{ratio:.4%} control stability; {len(variant_stable - control_union)} quad-only edges')


if __name__ == '__main__':
    main()
