"""Build and verify AFL++ feedback from librsvg's Rust SVG parser behind GdkPixbuf.

The overlay rebuilds the pinned GdkPixbuf and librsvg sources with librsvg's
Rust crates and SVG loader plugin carrying SanitizerCoverage pcguard edges.
The harness and GdkPixbuf are left uninstrumented, so every tuple that
afl-showmap reports on the valid control comes from the librsvg stack. No
campaign is started.
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


def main() -> None:
    base_receipt = PROJECT / 'verification.json'
    if not base_receipt.is_file() or not json.loads(base_receipt.read_text()).get('pass'):
        raise RuntimeError('base GdkPixbuf SVG project must be verified first')
    control = ROOT / MANIFEST['control']
    with docker_build_slot():
        run(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
             '-f', str(OVERLAY / 'Dockerfile'), '-t', IMAGE, str(PROJECT)])
    image_id = run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                   '--entrypoint', 'dpkg-query', IMAGE, '-W', '-f=${Version}', 'afl++'])
    if version != AFL_RELEASE:
        raise RuntimeError(f'AFL++ version mismatch: {version}')
    image_env = json.loads(run(['docker', 'image', 'inspect', IMAGE,
                                '--format', '{{json .Config.Env}}']))
    preload = next(item.partition('=')[2] for item in image_env
                   if item.startswith('AFL_PRELOAD='))
    entrypoint = MANIFEST['afl_entrypoint']
    if not MANIFEST.get('afl_file_input') or entrypoint != '/work/replay':
        raise RuntimeError('AFL++ SVG target must use one-shot /work/replay file input')
    observed = json.loads(run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                               *SANDBOX, '-e', f'LD_PRELOAD={preload}',
                               '-v', f'{control}:/input/control:ro',
                               '--entrypoint', '/work/replay', IMAGE, '/input/control']))
    if observed != MANIFEST['expected_output']:
        raise RuntimeError(f'AFL-instrumented build changed control result: {observed}')
    probe = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                            '-e', 'AFL_DUMP_MAP_SIZE=1', '-e', f'LD_PRELOAD={preload}',
                            '--entrypoint', entrypoint, IMAGE],
                           cwd=ROOT, capture_output=True, text=True)
    if not probe.stdout.strip().isdigit():
        raise RuntimeError(f'AFL++ map size probe failed: {probe.stderr[-2000:]}')
    map_size = int(probe.stdout.strip())
    with tempfile.TemporaryDirectory(prefix='parsarium-gdk-pixbuf-svg-afl-') as temporary:
        edges_path = Path(temporary) / 'edges.txt'
        showmap = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
             *SANDBOX, '-e', f'AFL_MAP_SIZE={map_size}',
             '-v', f'{control}:/input/control:ro', '-v', f'{temporary}:/coverage',
             '--entrypoint', 'afl-showmap', IMAGE,
             '-m', 'none', '-t', '30000', '-o', '/coverage/edges.txt', '--',
             entrypoint, '/input/control'],
             cwd=ROOT, capture_output=True, text=True)
        if showmap.returncode:
            raise RuntimeError(f'afl-showmap failed: {(showmap.stdout + showmap.stderr)[-3000:]}')
        if not re.search(r'Captured \d+ tuples', showmap.stdout + showmap.stderr):
            raise RuntimeError('afl-showmap did not report captured tuples')
        edges = sum(bool(line) for line in edges_path.read_text().splitlines())
    if edges < 2:
        raise RuntimeError(f'insufficient librsvg AFL++ feedback: {edges} edges')
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'librsvg_rust_pcguard_edges',
        'feedback_scope': 'librsvg 2.63.4 Rust crates and GdkPixbuf SVG loader plugin; harness and GdkPixbuf uninstrumented',
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'source_sha256': MANIFEST['source_sha256'],
        'underlying_source_sha256': MANIFEST['underlying_source_sha256'],
        'control_sha256': MANIFEST['control_sha256'],
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version, 'afl_version_output': version,
        'afl_preload': preload, 'afl_map_size': map_size,
        'afl_entrypoint': entrypoint, 'afl_file_input': True,
        'feedback_edges': edges,
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {edges} librsvg AFL++ feedback edges')


if __name__ == '__main__':
    main()
