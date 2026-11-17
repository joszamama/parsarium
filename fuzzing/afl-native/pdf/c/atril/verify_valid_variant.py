"""Check Atril PDF AFL++ feedback on two valid PDFs.

The control has two pages and a document information dictionary. The variant
has one page, a binary header comment and no information dictionary. Both are
valid, so any stable difference in edges or hit-count buckets comes from the
Atril backend and Poppler parser paths, not from error handling.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[5]
OVERLAY = Path(__file__).resolve().parent
PROJECT = ROOT / 'projects/pdf/c/atril'
IMAGE = 'parsarium-afl/pdf-c-atril:local'
CONTROL = ROOT / 'controls/pdf/two-page.pdf'
VARIANT = PROJECT / 'valid-one-page.pdf'
REPEATS = 3


def run(args: list[str]) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-2000:])
    return result.stdout


def sandbox(*args: str) -> list[str]:
    return ['docker', 'run', '--rm', '--platform', 'linux/arm64', '--network', 'none',
            '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--user', f'{os.getuid()}:{os.getgid()}',
            '--tmpfs', '/tmp:rw,exec,nosuid,size=64m', '--workdir', '/tmp', *args]


def output(sample: Path) -> dict:
    return json.loads(run(sandbox('-e', 'LD_PRELOAD=/work/install/lib/atril/3/backends/libpdfdocument.so',
                                  '-v', f'{sample}:/input/case:ro',
                                  '--entrypoint', '/work/replay', IMAGE, '/input/case')))


def guarded(path: str) -> bool:
    sections = run(sandbox('--entrypoint', 'readelf', IMAGE, '-SW', path))
    return '__sancov_guards' in sections


def afl_map(sample: Path, label: str, work: Path, map_size: int, repeat: int) -> set[str]:
    """Return 'edge:bucket' pairs so hit-count changes count as feedback."""
    destination = f'/coverage/{label}-{repeat}.map'
    run(sandbox('-e', f'AFL_MAP_SIZE={map_size}',
                '-v', f'{sample}:/input/case:ro', '-v', f'{work}:/coverage',
                '--entrypoint', 'afl-showmap', IMAGE, '-m', 'none', '-t', '10000',
                '-o', destination, '--', '/work/fuzzer', '/input/case'))
    return {line for line in (work / f'{label}-{repeat}.map').read_text().splitlines() if line}


def stability(maps: list[set[str]]) -> dict:
    return {'repeats': [len(m) for m in maps],
            'all_repeats_identical': all(m == maps[0] for m in maps),
            'stable_edges': len({p.split(':', 1)[0] for p in set.intersection(*maps)})}


def main() -> None:
    manifest = json.loads((PROJECT / 'manifest.json').read_text())
    overlay_receipt = json.loads((OVERLAY / 'verification.json').read_text())
    image_id = run(['docker', 'image', 'inspect', IMAGE, '--format', '{{.Id}}']).strip()
    if not overlay_receipt['pass'] or image_id != overlay_receipt['image_id']:
        raise RuntimeError('AFL++ image differs from verified overlay')
    if sha256(CONTROL.read_bytes()).hexdigest() != manifest['control_sha256']:
        raise RuntimeError('control changed')
    if sha256(VARIANT.read_bytes()).hexdigest() != manifest['valid_variant_sha256']:
        raise RuntimeError('valid variant changed')
    guard_scope = {
        '/work/replay': False,
        '/work/fuzzer': False,
        '/work/install/lib/libatrildocument.so': False,
        '/work/install/lib/libpoppler-glib.so': True,
        '/work/install/lib/libpoppler.so': True,
        '/work/install/lib/atril/3/backends/libpdfdocument.so': True,
    }
    observed_scope = {path: guarded(path) for path in guard_scope}
    if observed_scope != guard_scope:
        raise RuntimeError(f'AFL++ guards escaped PDF parser libraries: {observed_scope}')
    control_output, variant_output = output(CONTROL), output(VARIANT)
    if control_output != manifest['expected_output']:
        raise RuntimeError(f'control parsed unexpectedly: {control_output}')
    if variant_output != manifest['valid_variant_expected_output']:
        raise RuntimeError(f'valid variant parsed unexpectedly: {variant_output}')
    map_size = overlay_receipt['afl_map_size']
    with tempfile.TemporaryDirectory(prefix='parsarium-atril-pdf-valid-') as temporary:
        work = Path(temporary)
        control_maps = [afl_map(CONTROL, 'control', work, map_size, i) for i in range(REPEATS)]
        variant_maps = [afl_map(VARIANT, 'variant', work, map_size, i) for i in range(REPEATS)]
    control_stable, variant_stable = set.intersection(*control_maps), set.intersection(*variant_maps)
    control_any, variant_any = set.union(*control_maps), set.union(*variant_maps)
    edges = lambda pairs: {p.split(':', 1)[0] for p in pairs}
    stable_variant_only = variant_stable - control_any
    stable_control_only = control_stable - variant_any
    variant_only_edges = edges(variant_stable) - edges(control_any)
    control_only_edges = edges(control_stable) - edges(variant_any)
    bucket_changed = (edges(stable_variant_only) | edges(stable_control_only)) \
        - variant_only_edges - control_only_edges
    if not stable_variant_only and not stable_control_only:
        raise RuntimeError('valid variant does not change stable AFL++ feedback')
    receipt = {
        'schema_version': 1, 'project': 'pdf/c/atril', 'pass': True,
        'overlay_receipt_sha256': sha256((OVERLAY / 'verification.json').read_bytes()).hexdigest(),
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_sha256': manifest['source_sha256'],
        'control_sha256': manifest['control_sha256'],
        'control_output': control_output,
        'variant_sha256': manifest['valid_variant_sha256'],
        'variant_output': variant_output,
        'repeats': REPEATS,
        'control_stability': stability(control_maps),
        'variant_stability': stability(variant_maps),
        'stable_variant_only_edges': len(variant_only_edges),
        'stable_control_only_edges': len(control_only_edges),
        'stable_bucket_changed_edges': len(bucket_changed),
        'shared_parser_family': manifest['shared_parser_family'],
        'guarded_libraries': observed_scope,
    }
    (OVERLAY / 'valid-variant.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'Verified valid one-page variant: {len(variant_only_edges)} variant-only edges, '
          f'{len(control_only_edges)} control-only edges, '
          f'{len(bucket_changed)} edges with changed hit-count buckets')


if __name__ == '__main__':
    main()
