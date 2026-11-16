"""Build and verify AFL++ feedback from the pinned native PHP runtime."""

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
RELATIVE = OVERLAY.relative_to(ROOT / 'fuzzing/afl-native')
PROJECT = ROOT / 'projects' / RELATIVE
MANIFEST = json.loads((PROJECT / 'manifest.json').read_text())
IMAGE = f'parsarium-afl/{RELATIVE.parts[0]}-php-{RELATIVE.parts[2]}:local'


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f'{command[:5]} failed: {(result.stdout + result.stderr)[-3000:]}')
    return result.stdout.strip()


def main() -> None:
    base_receipt = PROJECT / 'verification.json'
    if not base_receipt.is_file() or not json.loads(base_receipt.read_text()).get('pass'):
        raise RuntimeError('base PHP runtime project must be verified first')
    control = ROOT / MANIFEST['control']
    run(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
         '-f', str(OVERLAY / 'Dockerfile'), '-t', IMAGE, str(ROOT)])
    image_id = run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = run(['docker', 'run', '--rm', '--entrypoint', 'dpkg-query', IMAGE,
                   '-W', '-f=${Version}', 'afl++'])
    if version != MANIFEST['fuzz_engine_release']:
        raise RuntimeError(f'AFL++ version mismatch: {version}')
    observed = json.loads(run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                               '--network', 'none', '--read-only', '--cap-drop', 'ALL',
                               '--security-opt', 'no-new-privileges',
                               '--user', f'{os.getuid()}:{os.getgid()}',
                               '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
                               '-e', 'LD_PRELOAD=/opt/imagick-afl/libaflrt.so',
                               '-v', f'{control}:/input/control:ro',
                               '--entrypoint', '/usr/bin/php', IMAGE,
                               '-d', 'extension=/opt/imagick-afl/imagick.so', '/work/control.php', '/input/control']))
    if observed != MANIFEST['expected_output']:
        raise RuntimeError(f'AFL-instrumented runtime changed control result: {observed}')
    with tempfile.TemporaryDirectory(prefix='parsarium-php-native-afl-') as temporary:
        edges_path = Path(temporary) / 'edges.txt'
        showmap = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
             '--network', 'none', '--read-only', '--cap-drop', 'ALL',
             '--security-opt', 'no-new-privileges',
             '--user', f'{os.getuid()}:{os.getgid()}',
             '--tmpfs', '/tmp:rw,exec,nosuid,size=64m',
             '-v', f'{control}:/input/control:ro', '-v', f'{temporary}:/coverage',
             '--entrypoint', 'afl-showmap', IMAGE,
             '-m', 'none', '-t', '30000', '-o', '/coverage/edges.txt', '--',
             '/work/fuzzer', '/input/control'],
             cwd=ROOT, capture_output=True, text=True)
        if showmap.returncode:
            raise RuntimeError(f'afl-showmap failed: {(showmap.stdout + showmap.stderr)[-3000:]}')
        match = re.search(r'Captured \d+ tuples \(map size (\d+)',
                          showmap.stdout + showmap.stderr)
        if not match:
            raise RuntimeError('afl-showmap did not report its map size')
        map_size = int(match.group(1))
        edges = sum(bool(line) for line in edges_path.read_text().splitlines())
    if edges < 2:
        raise RuntimeError(f'insufficient native PHP AFL++ feedback: {edges} edges')
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'native_pecl_imagick_source_edges',
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'source_sha256': MANIFEST['source_sha256'],
        'control_sha256': MANIFEST['control_sha256'],
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'afl_package': version, 'afl_map_size': map_size,
        'feedback_edges': edges,
        'overlay_file_sha256': {
            name: sha256((OVERLAY / name).read_bytes()).hexdigest()
            for name in ('Dockerfile', 'build.py', 'fuzzer')},
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {edges} native PHP AFL++ tuples')


if __name__ == '__main__':
    main()
