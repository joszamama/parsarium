"""Build and verify AFL++ feedback from pg_query's Rust path and the libpg_query parser it calls.

The overlay builds two afl.rs targets from the same harness: one where the vendored
libpg_query grammar, scanner and raw_parser entry (gram.c, scan.c, parser.c, checked by nm
in the image) carry trace-pc-guard, and one with only the Rust crates instrumented. On the
valid control, the first must report more AFL++ tuples than the second; the difference is
recorded as native feedback. No mutation campaign is started.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile
import tomllib


ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
RELATIVE = OVERLAY.relative_to(ROOT / 'fuzzing/afl-native')
PROJECT = ROOT / 'projects' / RELATIVE
MANIFEST = json.loads((PROJECT / 'manifest.json').read_text())
IMAGE = f'parsarium-afl/{RELATIVE.parts[0]}-{RELATIVE.parts[1]}-{RELATIVE.parts[2]}:local'
AFL_RELEASE = '4.33c-1.1ubuntu1'
AFL_RUST_RELEASE = '0.18.2'
OVERLAY_FILES = ('Cargo.toml', 'Cargo.lock', 'afl_fuzzer.rs', 'c-allowlist.txt', 'Dockerfile', 'build.py')


def run(command: list[str], *, input_data: bytes | None = None) -> str:
    result = subprocess.run(command, cwd=ROOT, input=input_data, capture_output=True)
    if result.returncode:
        output = (result.stdout + result.stderr).decode(errors='replace')
        raise RuntimeError(f'{command[:5]} failed: {output[-3000:]}')
    return result.stdout.decode(errors='replace').strip()


def sandbox(*extra: str) -> list[str]:
    return ['docker', 'run', '--rm', '-i', '--platform', MANIFEST['platform'],
            '--network', 'none', '--read-only', '--cap-drop', 'ALL',
            '--security-opt', 'no-new-privileges', '--user', f'{os.getuid()}:{os.getgid()}',
            '--tmpfs', '/tmp:rw,exec,nosuid,size=64m', '--workdir', '/tmp', *extra]


def map_size(target: str) -> int:
    probe = subprocess.run(['docker', 'run', '--rm', '--platform', MANIFEST['platform'],
                            '-e', 'AFL_DUMP_MAP_SIZE=1', '--entrypoint', target, IMAGE],
                           cwd=ROOT, capture_output=True, text=True)
    if not probe.stdout.strip().isdigit():
        raise RuntimeError(f'AFL++ map size probe failed for {target}')
    return int(probe.stdout.strip())


def control_edges(target: str, size: int, control: bytes) -> int:
    with tempfile.TemporaryDirectory(prefix='parsarium-pg-query-afl-') as temporary:
        os.chmod(temporary, 0o777)
        run(sandbox('-e', f'AFL_MAP_SIZE={size}', '-v', f'{temporary}:/coverage',
                    '--entrypoint', 'afl-showmap', IMAGE, '-m', 'none', '-t', '10000',
                    '-o', '/coverage/edges.txt', '--', target), input_data=control)
        return sum(bool(line) for line in (Path(temporary) / 'edges.txt').read_text().splitlines())


def main() -> None:
    base_receipt = PROJECT / 'verification.json'
    if not base_receipt.is_file() or not json.loads(base_receipt.read_text()).get('pass'):
        raise RuntimeError('base pg_query project must be verified first')
    lock = tomllib.loads((OVERLAY / 'Cargo.lock').read_text())['package']
    parser = [item for item in lock if (item['name'], item['version']) == ('pg_query', MANIFEST['release'])]
    if len(parser) != 1 or parser[0].get('checksum') != MANIFEST['source_sha256']:
        raise RuntimeError('AFL++ lockfile changed the pinned pg_query source')
    afl = [item for item in lock if (item['name'], item['version']) == ('afl', AFL_RUST_RELEASE)]
    if len(afl) != 1 or not afl[0].get('checksum'):
        raise RuntimeError('AFL++ Rust dependency is not locked')
    control = (ROOT / MANIFEST['control']).read_bytes()
    print(f'Building {IMAGE}', flush=True)
    run(['docker', 'build', '--quiet', '--platform', MANIFEST['platform'],
         '-f', str(OVERLAY / 'Dockerfile'), '-t', IMAGE, str(ROOT)])
    image_id = run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}'])
    version = run(['docker', 'run', '--rm', '--entrypoint', 'dpkg-query', IMAGE,
                   '-W', '-f=${Version}', 'afl++'])
    if version != AFL_RELEASE:
        raise RuntimeError(f'AFL++ version mismatch: {version}')
    observed = json.loads(run(sandbox('-v', f"{ROOT / MANIFEST['control']}:/input/control:ro",
                                      '--entrypoint', '/work/replay', IMAGE, '/input/control')))
    if observed != MANIFEST['expected_output']:
        raise RuntimeError(f'AFL-instrumented runtime changed control result: {observed}')
    objects = run(['docker', 'run', '--rm', '--entrypoint', 'cat', IMAGE,
                   '/work/afl-instrumented-objects.txt']).splitlines()
    full_map = map_size('/work/afl_fuzzer')
    rust_map = map_size('/work/afl_fuzzer_rust_only')
    full = control_edges('/work/afl_fuzzer', full_map, control)
    rust_only = control_edges('/work/afl_fuzzer_rust_only', rust_map, control)
    if full_map <= rust_map or full <= rust_only:
        raise RuntimeError(f'no native libpg_query AFL++ feedback: {full} tuples with C '
                           f'instrumentation, {rust_only} without')
    receipt = {
        'schema_version': 1, 'project': str(RELATIVE), 'pass': True,
        'feedback_kind': 'rust_and_native_libpg_query_parser_edges',
        'base_project_receipt_sha256': sha256(base_receipt.read_bytes()).hexdigest(),
        'overlay_file_sha256': {name: sha256((OVERLAY / name).read_bytes()).hexdigest()
                                for name in OVERLAY_FILES},
        'afl_package': version, 'afl_rust_release': AFL_RUST_RELEASE,
        'afl_rust_checksum': afl[0]['checksum'],
        'parser_source_sha256': MANIFEST['source_sha256'],
        'native_instrumented_objects': objects,
        'image_id': image_id, 'platform': MANIFEST['platform'],
        'control_sha256': MANIFEST['control_sha256'],
        'toolchain': run(['docker', 'run', '--rm', '--entrypoint', 'cat', IMAGE,
                          '/work/toolchain.txt']).splitlines(),
        'feedback_edges': full, 'afl_map_size': full_map,
        'rust_only_feedback_edges': rust_only, 'rust_only_afl_map_size': rust_map,
        'native_feedback_edges': full - rust_only,
    }
    (OVERLAY / 'verification.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified {RELATIVE}: {full} AFL++ tuples, {full - rust_only} from native libpg_query')


if __name__ == '__main__':
    main()
