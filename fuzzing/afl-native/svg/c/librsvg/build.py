"""Build and verify AFL++ feedback from librsvg's Rust SVG engine behind its C API.

The overlay rebuilds the pinned librsvg source with its Rust crates (the rsvg
SVG engine and the librsvg-c API crate) carrying SanitizerCoverage pcguard
edges. The harness is left uninstrumented, so every tuple that afl-showmap
reports comes from librsvg-2.so. A second valid SVG that swaps the control's
rects for a path must change the tuple set, which shows that the feedback
follows the parsed SVG content in the Rust engine rather than only the C entry
points. No campaign is started.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
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
IMAGE = f'parsarium-afl/{RELATIVE.parts[0]}-{RELATIVE.parts[1]}-{RELATIVE.parts[2]}:local'
AFL_RELEASE = '4.33c-1.1ubuntu1'
SANDBOX = ['--network', 'none', '--read-only', '--cap-drop', 'ALL',
           '--security-opt', 'no-new-privileges', '--user', f'{os.getuid()}:{os.getgid()}',
           '--tmpfs', '/tmp:rw,exec,nosuid,size=64m', '--workdir', '/tmp']


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'{command[:5]} failed: {(result.stdout + result.stderr)[-3000:]}')
    return result.stdout.strip()


def showmap(map_size: int, sample: Path) -> set[str]:
    with tempfile.TemporaryDirectory(prefix='parsarium-librsvg-svg-afl-') as temporary:
        result = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
             *SANDBOX, '-e', f'AFL_MAP_SIZE={map_size}',
             '-v', f'{sample}:/input/sample:ro', '-v', f'{temporary}:/coverage',
             '--entrypoint', 'afl-showmap', IMAGE,
             '-m', 'none', '-t', '30000', '-o', '/coverage/edges.txt', '--',
             '/work/fuzzer', '/input/sample'],
             cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(f'afl-showmap failed: {(result.stdout + result.stderr)[-3000:]}')
        if not re.search(r'Captured \d+ tuples', result.stdout + result.stderr):
            raise RuntimeError('afl-showmap did not report captured tuples')
        return {line.partition(':')[0] for line in
                (Path(temporary) / 'edges.txt').read_text().splitlines() if line}


def main() -> None:
    base_receipt = PROJECT / 'verification.json'
    if not base_receipt.is_file() or not json.loads(base_receipt.read_text()).get('pass'):
        raise RuntimeError('base librsvg SVG project must be verified first')
    control = ROOT / MANIFEST['control']
    variant = OVERLAY / 'valid-path.svg'
    with docker_build_slot():
        run(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
             '-f', str(OVERLAY / 'Dockerfile'), '-t', IMAGE, str(PROJECT)])
    image_id = run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                   '--entrypoint', 'dpkg-query', IMAGE, '-W', '-f=${Version}', 'afl++'])
    if version != AFL_RELEASE:
        raise RuntimeError(f'AFL++ version mismatch: {version}')
    observed = json.loads(run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                               *SANDBOX, '-v', f'{control}:/input/control:ro',
                               '--entrypoint', '/work/replay', IMAGE, '/input/control']))
    if observed != MANIFEST['expected_output']:
        raise RuntimeError(f'AFL-instrumented build changed control result: {observed}')
    variant_output = json.loads(run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                                     *SANDBOX, '-v', f'{variant}:/input/variant:ro',
                                     '--entrypoint', '/work/replay', IMAGE, '/input/variant']))
    if variant_output != {'width': 2, 'height': 1, 'first': [0, 0, 255], 'second': [0, 0, 255]}:
        raise RuntimeError(f'valid path variant rendered unexpectedly: {variant_output}')
    probe = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                            '-e', 'AFL_DUMP_MAP_SIZE=1', '--entrypoint', '/work/fuzzer', IMAGE],
                           cwd=ROOT, capture_output=True, text=True)
    if not probe.stdout.strip().isdigit():
        raise RuntimeError(f'AFL++ map size probe failed: {probe.stderr[-2000:]}')
    map_size = int(probe.stdout.strip())
    control_maps = [showmap(map_size, control) for _ in range(3)]
    variant_maps = [showmap(map_size, variant) for _ in range(3)]
    control_edges, variant_edges = control_maps[0], variant_maps[0]
    control_stable = set.intersection(*control_maps)
    variant_stable = set.intersection(*variant_maps)
    control_union = set.union(*control_maps)
    if len(control_edges) < 2:
        raise RuntimeError(f'insufficient librsvg AFL++ feedback: {len(control_edges)} edges')
    if control_edges == variant_edges:
        raise RuntimeError('valid rect and path SVGs produced identical librsvg feedback')
    if not variant_stable - set.union(*control_maps):
        raise RuntimeError('valid path SVG produced no stable new parser feedback')
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'librsvg_rust_pcguard_edges',
        'feedback_scope': 'librsvg 2.63.4 Rust crates (rsvg SVG engine and librsvg-c API) in librsvg-2.so; harness uninstrumented',
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'source_sha256': MANIFEST['source_sha256'],
        'control_sha256': MANIFEST['control_sha256'],
        'variant_sha256': sha256(variant.read_bytes()).hexdigest(),
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version, 'afl_version_output': version,
        'afl_map_size': map_size,
        'feedback_edges': len(control_edges),
        'variant_feedback_edges': len(variant_edges),
        'edges_only_in_control': len(control_edges - variant_edges),
        'edges_only_in_variant': len(variant_edges - control_edges),
        'control_repeat_edge_counts': [len(edges) for edges in control_maps],
        'control_stable_edges': len(control_stable),
        'control_union_edges': len(control_union),
        'variant_repeat_edge_counts': [len(edges) for edges in variant_maps],
        'stable_variant_only_edges': len(variant_stable - control_union),
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py', 'valid-path.svg')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {len(control_edges)} librsvg AFL++ feedback edges')


if __name__ == '__main__':
    main()
